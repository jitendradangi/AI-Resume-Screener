# Audit Notes — Part 3: AI/ATS/Matching Deep Dive, Frontend, End-to-End & Roadmap
> Source: Cowork session (code-inspected). Live API, DB, and Groq not verified unless stated.
> Severity: P0 = app-breaking, P1 = major feature broken, P2 = security/data gap, P3 = low/cosmetic.

---

## 1. AI & Groq Integration

### Configuration Mismatch
| File | Model Value |
|------|-------------|
| `backend/.env` (live) | `openai/gpt-oss-120b` (real key present) |
| `backend/.env.example` | `llama-3.3-70b-versatile` |
| `backend/.env.testing` | `llama-3.3-70b-versatile` |
| `backend/app/config.py` default | `llama-3.3-70b-versatile` |
| `resume_analyzer.py` fallback | `llama-3.3-70b-versatile` |
| `semantic_matcher.py` fallback | `llama-3.3-70b-versatile` |
| `test_groq_config.py` | `llama-3.3-70b-versatile` |

**Risk:** `openai/gpt-oss-120b` on Groq — it is unverified whether this model supports `response_format={"type": "json_object"}`. Both AI modules use JSON mode. If the model does not support it, every AI analysis call fails. `llama` models are confirmed to support JSON mode.

### Duplicated Groq Client Code
- `resume_analyzer.py` has its own `get_groq_client()` and `get_groq_model()`
- `semantic_matcher.py` has its own `get_groq_client()` and `get_groq_model()`
- These are identical implementations duplicated across two files instead of using `llm_service.py` (which is 0 bytes)

### Error Handling Gaps
- Catches `"does not exist"` / `"access"` / `"model_not_found"` → `RuntimeError` with guidance
- All other errors: generic `RuntimeError`
- No retry logic
- No Groq rate-limit handling
- No timeout configuration

### Response Validation Gap
- `parse_response` in `resume_analyzer.py` only requires `{overall_score, strengths, weaknesses, recommendations}`
- `score_breakdown` is **optional** in validation
- If Groq returns an abbreviated response, it passes validation and the frontend displays all score components as 0
- No enforcement that `score_breakdown` must contain all four sub-scores

### Stale / Wrong References
| Location | Wrong Claim | Actual |
|----------|-------------|--------|
| `resume_analyzer.py` docstring | "Gemini" | Groq |
| Resume router comments | "Call Gemini (Step 4 prompt → Step 5 JSON parse)" | Groq |
| `frontend/src/components/Sidebar.jsx:117` | "GPT-4 Analysis Ready" | Groq |
| `README.md`, `CHANGELOG.md` | "Google Gemini AI" | Groq |
| `config.py` | `GEMINI_API_KEY` field | Unused; no Gemini code anywhere |
| `semantic_matcher.py` | `import warnings` comment about `google-generativeai FutureWarning` | Never imports it — dead comment |

---

## 2. ATS Scoring — Two Parallel Systems

### System A: AI-Based (Groq)
- **Trigger:** `POST /resume/{id}/ai-analysis`
- **Storage:** `ai_analysis` JSON column on `ResumeAnalysis` table
- **Score structure:** `overall_score` (0–100) + `score_breakdown` with 4 sub-scores each out of 25:
  - `content_quality` /25, `skills_relevance` /25, `experience_depth` /25, `formatting_clarity` /25
- **Frontend:** ATSScore.jsx reads ONLY this system. Progress bars use `(value/25)*100`.
  - **Risk:** If Groq ever returns sub-scores on 0–100 scale, bars display 400% and break UI.

### System B: Deterministic ATS
- **Trigger:** `POST /resume/{id}/ats-score` (manual) or `POST /resume/{id}/ats-score/auto`
- **Storage:** `ats_scores` table
- **Components:** 7 scorers — skills (.25), experience (.20), education (.15), keyword (.15), format (.10), section (.10), projects (.05). Weights sum to 1.0. ✅

### Weighting Inconsistency Between Two Paths
| Component | `OverallScorer` weight | `generate_score_auto` weight |
|-----------|----------------------|------------------------------|
| Skills | 0.25 | 0.25 |
| Keyword | 0.15 | 0.20 |
| Education | 0.15 | 0.20 |
| Experience | 0.20 | 0.15 |
| Projects | 0.05 | 0.10 |
| Format | 0.10 | 0.05 |
| Section | 0.10 | 0.05 |

Same resume gets a **different overall score** depending on which path was used. Not documented.

### Frontend vs Backend Disconnect
- Frontend has **no `atsService`** — zero calls to System B endpoints
- `ats_scores` table is **completely unused** by the frontend
- `generate_report` (fully automatic path via ATS router) is not accessible to frontend (no ownership check, no frontend service)
- `score_exists` prevents re-generation — no upsert available

### ATS Persistence Issue
- `processing_status` is **never set to `COMPLETED`** anywhere in the codebase (confirmed by grep)
- Only `PENDING` assignment exists in `resume.py` service
- Every resume shows `PENDING` status forever in the dashboard

---

## 3. Job Matching — Confirmed Bugs & Status

### Critical: generate_skill_match Always Crashes (B-01 re-confirmed)
- `job_match.py:169`: `ats_score_repository.get_by_resume(self.db, resume.id)`
- `ATSScoreRepository` methods: `get_by_resume_analysis`, `get_by_public_id`, `score_exists`, `get_by_min_score`, `get_top_scores`, `create_score`, `update_score`
- `get_by_resume` **does not exist** → `AttributeError` on every call
- `match_resume_to_jobs` catches `ValueError` only → `AttributeError` propagates → 500
- **Effect:** `POST /matches/generate/{r}/{j}` always returns 500

### JobMatchResponse Schema Drops All Component Data
- `JobMatchResponse` exposes: `public_id`, `created_at`, `match_score`, `recommendation`, `skills{matched, missing}`, `resume_public_id`, `job_public_id`
- **Dropped silently:** `experience_match_score`, `education_match_score`, `project_match_score`, `semantic_score`, `match_level`, `matched_preferred_skills`, all component breakdowns
- `MatchDetails.jsx` reads `match.component_scores?.skills`, `.experience`, `.education`, `.projects`
- These fields **do not exist** in `JobMatchResponse` → always `undefined` → component bars always show 0%
- `JobRecommendation` schema (used by dashboard/jobs page) **does** expose `component_scores` — so that path works

### Duplicate Column Definitions (Confirmed)
| Column | Lines defined |
|--------|--------------|
| `experience_match_score` | 73, 118 |
| `education_match_score` | 86, 120 |
| `project_match_score` | 97, 122 |
| `semantic_score` vs `semantic_match_score` | 102, 124 |
| `match_score` vs `overall_match` | Both set to same value in `generate_skill_match` lines ~255, ~281 |

SQLAlchemy uses last definition. All are model-level duplicates.

### No External Job Feed
- All jobs are user-created only
- No third-party job API integration exists anywhere in codebase
- Dashboard recommendations only appear if the user has created jobs themselves

### RecommendationEngine Design Smell (Confirmed)
- `RecommendationEngine` passes the same `ats_score` (resume quality score) as the ATS component for **every job** in a recommendation list
- It is not computed per-job — every recommendation has an identical ATS component value

---

## 4. Frontend Audit

### Auth & Routing
| Item | Status | Notes |
|------|--------|-------|
| Auth context | ✅ Implemented | JWT stored in localStorage |
| ProtectedRoute | ✅ Working | Redirects to `/` (Login) |
| Token storage | ⚠️ localStorage | XSS risk; no httpOnly cookie |
| Profile.jsx logout | ⚠️ Partial | Uses `localStorage.removeItem("token")` directly, not `context.logout()`. Token remains in React context state until page reload. |
| Duplicate routes | ⚠️ Bug | `/ats-score` and `/ats-score/:public_id` both registered |

### Page-by-Page Status

| Page | Backend Endpoint | Request Matches | Response Matches | Loading State | Error State | Overall |
|------|-----------------|----------------|-----------------|---------------|-------------|---------|
| Login | POST /auth/login | ✅ | ✅ | ✅ | ✅ | WORKING |
| Register | POST /auth/register | ✅ | ✅ | ✅ | ✅ | WORKING |
| Dashboard | GET /resume/my-resumes, GET /matches/recommendations | ✅ | ✅ (recommendations) | ✅ | Partial | PARTIAL — ATS card needs ai_analysis run first; jobs card empty if no user-created jobs |
| Resume Upload | POST /resume/upload | ✅ | ✅ | ✅ | ✅ | WORKING |
| My Resumes | GET /resume/my-resumes | ✅ | ✅ | ✅ | ✅ | WORKING |
| Resume Details | GET /resume/{id} | ✅ | ✅ | ✅ | ✅ | WORKING |
| ATSScore | POST /resume/{id}/ai-analysis | ✅ | ✅ (risk: score_breakdown optional) | ✅ | Partial | PARTIAL — works if Groq key valid & model supports JSON mode |
| Jobs | GET /jobs/open + /matches/recommendations | ✅ | ✅ | ✅ | Partial | PARTIAL — jobs empty unless user created jobs |
| Match Details | GET /matches/{r}/{j}, POST /matches/generate | ✅ request | ❌ response mismatch | ✅ | ✅ | **BROKEN** — generate always 500 (B-01); component scores always 0% (schema mismatch) |
| Profile | GET/PUT /user/profile | ✅ | ✅ | ✅ | ✅ | WORKING |
| Settings | — | N/A | N/A | — | — | UNKNOWN — not confirmed in audit |
| Navigation / Sidebar | — | — | — | — | — | Has "GPT-4 Analysis Ready" hardcoded (line 117) |

### Environment / Build Issues
| Issue | Severity |
|-------|----------|
| `VITE_API_BASE_URL=http://localhost:8000` hardcoded in `frontend/.env` — no env switching, no `.env.example` | P1 — frontend cannot be deployed without manual change |
| `frontend/dist/` built 2026-09-04 — stale vs source (modified since) | P2 — deployed build is out of sync |
| No `frontend/.env.production` or `frontend/.env.example` | P2 |
| If `VITE_API_BASE_URL` is missing, Axios `baseURL` is `undefined` → all API calls use relative URLs | P2 |

---

## 5. End-to-End Journey Verification

| User Journey | First Failure Point | Outcome |
|-------------|-------------------|---------|
| Register → Login → View Dashboard | None in auth sub-journey | ✅ Works |
| Upload Resume → View in My Resumes | None | ✅ Works — but `processing_status` stays PENDING forever |
| Upload → Auto-parse → AI Analysis → View ATS Score | No auto-parse after upload; each step is a manual API call not triggered by upload | ⚠️ Partial — user must manually trigger each step; works if done manually |
| AI Analysis → ATSScore page | Works IF Groq key valid and `gpt-oss-120b` supports JSON mode | ⚠️ At-risk |
| Jobs page → View recommendations | Works deterministically — no Groq needed | ✅ Works IF user has created jobs |
| Match Details → Generate Match | `POST /matches/generate` → 500 (B-01 `AttributeError`) | ❌ Always broken |
| Match Details → View component scores | `JobMatchResponse` drops all component data | ❌ Always shows 0% |
| Dashboard ATS card | Requires ai_analysis to have been run | ⚠️ Conditional |
| Dashboard job matches | Requires user-created jobs to exist | ⚠️ Conditional |

---

## 6. Security Findings

| # | Issue | Severity | Location |
|---|-------|----------|----------|
| S-01 | JWT stored in `localStorage` — vulnerable to XSS. Any injected script can steal the token. | P2 | Frontend auth context |
| S-02 | File upload uses only extension + `Content-Type` validation. No magic-byte (binary signature) check. `Content-Type` can be spoofed to upload malicious files with a valid extension. | P2 | `backend/app/routers/resume.py` |
| S-03 | `GET /jobs/search` returns DRAFT and CLOSED jobs publicly (no status filter). | P2 | `backend/app/services/job.py` |
| S-04 | 8 endpoints have no ownership check (see Part 2 Section 4). User A can generate matches for User B's resume+job. | P2 | Multiple routers |
| S-05 | `GET /profile` (main.py) returns raw ORM User object with no `response_model`. May expose internal fields. Serialization behavior unverified. | P2 | `backend/app/main.py:~124` |
| S-06 | Rate limiting entirely non-functional (`SlowAPIMiddleware` not added). No brute-force protection on `/auth/login` or `/auth/register`. | P1 | `backend/app/main.py` |
| S-07 | CORS `allow_credentials=True` with `allow_methods=["*"]` and `allow_headers=["*"]`. Review whether all methods/headers need to be open with credentials. | P3 | `backend/app/main.py` |
| S-08 | No email verification on registration. | P3 | `backend/app/routers/auth.py` |
| S-09 | `PUT /user/profile` allows password change without re-authentication. | P3 | `backend/app/routers/user.py` |
| S-10 | Upload directory is a relative path (`uploads/` from CWD). No explicit path traversal protection beyond UUID-prefixed filenames. | P3 | `backend/app/routers/resume.py` |

---

## 7. Testing Status

| Test File | Type | Tests | Runnable | Covers |
|-----------|------|-------|----------|--------|
| `test_groq_config.py` | Unit | 7 | Not run (no env with deps) | Groq config validation only |
| `test_profile_api.py` | Ad-hoc script | — | Requires live DB + hardcoded email | Profile API manual test |
| `test_user_service.py` | Ad-hoc script | — | Requires live DB + hardcoded email | User service manual test |
| `backend/test` | 0-byte file (not a dir) | — | N/A | Nothing |

**Coverage gaps:** Auth, resume upload, parsing, ATS scoring, job matching, job CRUD, AI analysis, database models — **zero automated tests**.

---

## 8. Deployment & Configuration

| Item | Status | Notes |
|------|--------|-------|
| Railway backend | Deployed | `nixpacks.toml` present |
| `PRODUCTION_CONFIG.md` | Present | Documents Railway setup |
| `docker-compose.yml` | Present | Uses `.env.development`, `MYSQL_ROOT_PASSWORD` |
| Backend `.env` | Present, gitignored ✅ | Contains real `DATABASE_URL`, `SECRET_KEY`, `GROQ_API_KEY` — not exposed |
| Frontend `.env` | `localhost:8000` hardcoded | No `.env.example`, no production env file |
| Frontend dist | Stale (built 2026-09-04) | Source modified since; needs rebuild |
| Alembic | Missing | No migration tooling; schema via `create_all` + ad-hoc scripts |
| Health check endpoint | `GET /` exists | Returns `{message}` but has broken rate-limit decorator |
| Logging | `logs/app.log` + `error.log` (relative path) | Real logs present; not read during audit to avoid exposing credentials |

---

## 9. Feature Inventory — Overall Status

| Feature | Backend | Frontend | Database | Integration | Overall |
|---------|---------|----------|----------|-------------|---------|
| User Registration | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | ✅ COMPLETE |
| User Login / JWT | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | NOT APPLICABLE | COMPLETE AND VERIFIED | ✅ COMPLETE |
| Protected Routes | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | NOT APPLICABLE | COMPLETE AND VERIFIED | ✅ COMPLETE |
| Logout | IMPLEMENTED BUT UNVERIFIED | PARTIALLY IMPLEMENTED | NOT APPLICABLE | PARTIALLY IMPLEMENTED | ⚠️ PARTIAL — context not updated |
| Token Expiry | IMPLEMENTED BUT UNVERIFIED | NOT APPLICABLE | NOT APPLICABLE | NOT APPLICABLE | ⚠️ UNVERIFIED |
| Authorization / Ownership | PARTIALLY IMPLEMENTED | NOT APPLICABLE | NOT APPLICABLE | NOT APPLICABLE | ⚠️ PARTIAL — 8 endpoints missing checks |
| Resume Upload | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | ✅ COMPLETE |
| File Validation | PARTIALLY IMPLEMENTED | PARTIALLY IMPLEMENTED | NOT APPLICABLE | PARTIALLY IMPLEMENTED | ⚠️ PARTIAL — no magic-byte check |
| Resume List / Detail | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | ✅ COMPLETE |
| Resume Update / Delete | IMPLEMENTED BUT UNVERIFIED | NOT APPLICABLE | PARTIALLY IMPLEMENTED | NOT APPLICABLE | ⚠️ PARTIAL — delete may fail if ATSScore exists (B-03) |
| PDF/DOCX Text Extraction | IMPLEMENTED BUT UNVERIFIED | NOT APPLICABLE | NOT APPLICABLE | NOT APPLICABLE | ⚠️ UNVERIFIED — endpoint exists, not frontend-wired |
| Resume Section Parsing | IMPLEMENTED BUT UNVERIFIED | MISSING | NOT APPLICABLE | MISSING | ⚠️ PARTIAL — no frontend consumer |
| Structured Data Extraction | IMPLEMENTED BUT UNVERIFIED | MISSING | NOT APPLICABLE | MISSING | ⚠️ PARTIAL — no frontend consumer |
| Processing Status | BROKEN | PARTIALLY IMPLEMENTED | COMPLETE AND VERIFIED | BROKEN | ❌ BROKEN — always PENDING |
| AI Resume Analysis (Groq) | IMPLEMENTED BUT UNVERIFIED | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | IMPLEMENTED BUT UNVERIFIED | ⚠️ AT-RISK — JSON mode unverified for gpt-oss-120b |
| ATS Score (AI path) | IMPLEMENTED BUT UNVERIFIED | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | IMPLEMENTED BUT UNVERIFIED | ⚠️ AT-RISK |
| ATS Score (Deterministic) | IMPLEMENTED BUT UNVERIFIED | MISSING | COMPLETE AND VERIFIED | MISSING | ⚠️ PARTIAL — no frontend service |
| Automatic Upload Pipeline | MISSING | MISSING | NOT APPLICABLE | MISSING | ❌ MISSING |
| Job Create / List / Detail | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | ✅ COMPLETE |
| Job Update / Delete | COMPLETE AND VERIFIED | NOT APPLICABLE | COMPLETE AND VERIFIED | NOT APPLICABLE | ✅ COMPLETE |
| Job Search | BROKEN | COMPLETE AND VERIFIED | NOT APPLICABLE | BROKEN | ❌ BROKEN — leaks DRAFT/CLOSED jobs |
| External Job Feed | MISSING | MISSING | MISSING | MISSING | ❌ MISSING |
| Job Description Parsing | IMPLEMENTED BUT UNVERIFIED | MISSING | NOT APPLICABLE | MISSING | ⚠️ PARTIAL |
| Job Match Generation | BROKEN | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | BROKEN | ❌ BROKEN — always 500 (B-01) |
| Match Component Scores | IMPLEMENTED BUT UNVERIFIED | BROKEN | COMPLETE AND VERIFIED | BROKEN | ❌ BROKEN — schema drops all components |
| Job Recommendations | IMPLEMENTED BUT UNVERIFIED | COMPLETE AND VERIFIED | COMPLETE AND VERIFIED | IMPLEMENTED BUT UNVERIFIED | ⚠️ UNVERIFIED — works if jobs exist |
| Semantic Matching | PARTIALLY IMPLEMENTED | MISSING | NOT APPLICABLE | MISSING | ⚠️ PARTIAL — optional/swallowed on error |
| Match Details Page | BROKEN | COMPLETE AND VERIFIED | NOT APPLICABLE | BROKEN | ❌ BROKEN — 500 on generate; 0% on display |
| ATSScore Page | IMPLEMENTED BUT UNVERIFIED | COMPLETE AND VERIFIED | NOT APPLICABLE | IMPLEMENTED BUT UNVERIFIED | ⚠️ AT-RISK |
| Rate Limiting | BROKEN | NOT APPLICABLE | NOT APPLICABLE | NOT APPLICABLE | ❌ BROKEN — middleware missing |
| Admin Functionality | MISSING | MISSING | MISSING | MISSING | ❌ MISSING |
| Email Verification | MISSING | MISSING | MISSING | MISSING | ❌ MISSING |
| Automated Tests | MISSING | MISSING | MISSING | MISSING | ❌ MISSING |

---

## 10. Prioritized Roadmap

### P0 — Must Fix Before Any Feature Works

| # | Fix | File / Location |
|---|-----|----------------|
| R-01 | Add `get_by_resume(db, resume_id)` to `ATSScoreRepository` OR change `job_match.py:169` to use `get_by_resume_analysis` with correct param | `backend/app/repositories/ats_score.py`, `backend/app/services/job_match.py:169` |
| R-02 | Add `app.add_middleware(SlowAPIMiddleware)` and import it in `main.py` | `backend/app/main.py` |

### P1 — Core Features Broken or Risky

| # | Fix | File / Location |
|---|-----|----------------|
| R-03 | Add `ondelete="CASCADE"` to `ATSScore.resume_analysis_id` FK to prevent `IntegrityError` on resume delete | `backend/app/models/ats_score.py` |
| R-04 | Add `component_scores`, `experience_match_score`, `education_match_score`, `project_match_score`, `semantic_score`, `match_level` to `JobMatchResponse` schema | `backend/app/schemas/job_match.py` |
| R-05 | Add status filter to `search_jobs` — only return `OPEN` jobs | `backend/app/repositories/job.py` or `services/job.py` |
| R-06 | Set `processing_status = COMPLETED` after successful parse/extract in resume service | `backend/app/services/resume.py` |
| R-07 | Create `frontend/.env.example` and `frontend/.env.production` with correct Railway backend URL | `frontend/` |
| R-08 | Verify `openai/gpt-oss-120b` supports `json_object` response format on Groq, or switch to a confirmed model | `backend/.env`, `backend/app/ai/resume_analyzer.py` |

### P2 — Security & Authorization

| # | Fix | File / Location |
|---|-----|----------------|
| R-09 | Add ownership checks to `/resume/{id}/parse`, `/resume/{id}/sections`, all `/resume/{id}/ats` (ATS router), and all `/matches/` endpoints | Multiple routers |
| R-10 | Add magic-byte validation to file upload (validate actual file bytes, not just Content-Type) | `backend/app/routers/resume.py` |
| R-11 | Add `response_model=UserResponse` and remove the duplicate `/profile` route from `main.py` | `backend/app/main.py:~124` |
| R-12 | Make `ATSScoreResponse` populate `resume_analysis_public_id` (add relationship to model or join in service) | `backend/app/models/ats_score.py`, `backend/app/schemas/ats_score.py` |
| R-13 | Remove duplicate route registrations in `job_match.py` (lines 135–159 and 225–255) | `backend/app/routers/job_match.py` |

### P3 — Quality & Cleanup

| # | Fix | File / Location |
|---|-----|----------------|
| R-14 | Consolidate Groq client init into `llm_service.py`; remove duplicates from `resume_analyzer.py` and `semantic_matcher.py` | `backend/app/ai/` |
| R-15 | Replace all "Gemini", "GPT-4" references with "Groq"; remove `GEMINI_API_KEY` from config | README, Sidebar.jsx:117, resume_analyzer.py docstring, router comments, config.py |
| R-16 | Align `OverallScorer` and `generate_score_auto` weights OR document the difference | `backend/app/ats/overall_scorer.py`, `backend/app/services/ats_score.py` |
| R-17 | Wire `atsService` in frontend to consume deterministic ATS (`/resume/{id}/ats-score`) OR remove System B entirely and use only AI scoring | `frontend/src/services/` |
| R-18 | Add automatic pipeline trigger: upload → parse → extract on upload completion | `backend/app/services/resume.py` |
| R-19 | Fix `Profile.jsx` logout to call `context.logout()` instead of direct `localStorage.removeItem` | `frontend/src/pages/Profile.jsx` |
| R-20 | Remove duplicate `/ats-score` route in frontend router | `frontend/src/App.jsx` or router file |
| R-21 | Add Alembic for proper migration management | `backend/` |
| R-22 | Remove/fix `ResumeRepository.get_active_resumes` (references non-existent `is_active` column) | `backend/app/repositories/resume.py` |
| R-23 | Remove `RateLimitExceeded` duplicate handler registration (line ~55) | `backend/app/main.py:55` |
| R-24 | Add `app/ai/__init__.py` package marker | `backend/app/ai/` |
| R-25 | Replace `@app.on_event` with lifespan context | `backend/app/main.py` |
| R-26 | Write tests: auth, upload, ATS, matching, job CRUD — `backend/test` (0-byte file) must be deleted and replaced with a `tests/` directory | `backend/` |

---

## 11. Could Not Verify

- Live database schema (FK enforcement, column presence, index definitions)
- Groq API response format for `openai/gpt-oss-120b` with `json_object`
- Whether stale `frontend/dist/` is what Railway serves or if it rebuilds
- `Settings` page — existence and functionality not confirmed
- Actual Railway runtime logs and live error rates
- Backend test suite execution (no Python env with deps available during audit)
- Whether `semantic_matcher.py` `import warnings` dead comment causes any import issues