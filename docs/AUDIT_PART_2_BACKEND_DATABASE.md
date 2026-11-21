# Audit Notes — Part 2: AI, ATS, Jobs, Matching, Backend Deep Dive
> Source: Cowork session (code-inspected). DB and live API not verified unless stated.
> Severity: P0 = app-breaking, P1 = major feature broken, P2 = security/data gap, P3 = low/cosmetic.

---

## 1. Complete API Endpoint Inventory

| # | Method | Path | Auth | Ownership | Response Model | Notes |
|---|--------|------|------|-----------|----------------|-------|
| 1 | POST | /auth/register | None | — | UserResponse | |
| 2 | POST | /auth/login | None | — | TokenResponse | OAuth2PasswordRequestForm |
| 3 | POST | /resume/upload | ✅ | — | ResumeResponse | |
| 4 | GET | /resume/my-resumes | ✅ | — | List[ResumeResponse] | |
| 5 | GET | /resume/{public_id} | ✅ | ✅ | ResumeResponse | |
| 6 | PUT | /resume/{public_id} | ✅ | ✅ | ResumeResponse | |
| 7 | DELETE | /resume/{public_id} | ✅ | ✅ | {success, message} | |
| 8 | POST | /resume/{public_id}/parse | ✅ | ❌ MISSING | {success, text} | Auth but no ownership |
| 9 | POST | /resume/{public_id}/sections | ✅ | ❌ MISSING | {success, sections} | Auth but no ownership |
| 10 | POST | /resume/{public_id}/extract | ✅ | ✅ | {success, public_id, data} | |
| 11 | POST | /resume/{public_id}/analyze | ✅ | ✅ | {success, message, result} | |
| 12 | POST | /resume/{public_id}/ai-analysis | ✅ | ✅ | AIAnalysisResponse | Groq call |
| 13 | POST | /resume/{public_id}/ats-score | ✅ | ✅ | ATSScoreResponse | Manual input |
| 14 | POST | /resume/{public_id}/ats-score/auto | ✅ | ✅ | ATSScoreResponse | |
| 15 | POST | /resume/{public_id}/ats | ✅ | ❌ MISSING | ATSScoreResponse | ATS router, no ownership |
| 16 | GET | /resume/{public_id}/ats | ✅ | ❌ MISSING | ATSScoreResponse | ATS router, no ownership |
| 17 | PUT | /resume/{public_id}/ats | ✅ | ❌ MISSING | ATSScoreResponse | ATS router, no ownership |
| 18 | POST | /jobs/ | ✅ | — | JobResponse | |
| 19 | GET | /jobs/ | ✅ | — | List[JobResponse] | User's own jobs |
| 20 | GET | /jobs/open | None | — | List[JobResponse] | Public |
| 21 | GET | /jobs/search | None | — | List[JobResponse] | Public; no status filter (bug) |
| 22 | GET | /jobs/{public_id} | ✅ | ✅ | JobResponse | |
| 23 | PUT | /jobs/{public_id} | ✅ | ✅ | JobResponse | |
| 24 | DELETE | /jobs/{public_id} | ✅ | ✅ | {success, message} | |
| 25 | POST | /jobs/{public_id}/parse | ✅ | ✅ | {public_id, parsed_data} | |
| 26 | POST | /matches | ✅ | ❌ MISSING | JobMatchResponse | No ownership check |
| 27 | GET | /matches/resume/{resume_public_id} | ✅ | ❌ MISSING | List[JobMatchResponse] | |
| 28 | GET | /matches/job/{job_public_id} | ✅ | ❌ MISSING | List[JobMatchResponse] | FIRST registered; duplicate at line 141 is dead |
| 29 | GET | /matches/job/{job_public_id} | ✅ | — | — | ⚠️ DEAD ROUTE (duplicate, line 141) |
| 30 | GET | /matches/recommendations/{resume_public_id} | ✅ | ❌ MISSING | List[JobRecommendation] | FIRST registered |
| 31 | GET | /matches/recommendations/{resume_public_id} | — | — | — | ⚠️ DEAD ROUTE (duplicate, line 225) |
| 32 | GET | /matches/{resume_public_id}/{job_public_id} | ✅ | ❌ MISSING | JobMatchResponse | |
| 33 | POST | /matches/generate/{resume_public_id}/{job_public_id} | ✅ | ❌ MISSING | JobMatchResponse | |
| 34 | GET | /user/profile | ✅ | — | UserResponse | |
| 35 | PUT | /user/profile | ✅ | — | UserResponse | |
| 36 | GET | / | ⚠️ Rate limit (broken) | — | {message} | |
| 37 | GET | /profile | ⚠️ Rate limit (broken) | — | ❌ No response_model | Raw ORM object; duplicates #34 |

---

## 2. Frontend API Coverage

| Frontend Consumer | Endpoint Called | Status |
|-------------------|----------------|--------|
| login.jsx | POST /auth/login | ✅ Used |
| register.jsx | POST /auth/register | ✅ Used |
| resumeService.js | POST /resume/upload | ✅ Used |
| resumeService.js | GET /resume/my-resumes | ✅ Used |
| resumeService.js | GET /resume/{id} | ✅ Used |
| resumeService.js | POST /resume/{id}/ai-analysis | ✅ Used |
| jobService.js | GET /jobs/open | ✅ Used |
| jobService.js | GET /jobs/search | ✅ Used |
| jobService.js | GET/POST /jobs/ | ✅ Used |
| jobService.js | GET /jobs/{id} | ✅ Used |
| jobService.js | GET /matches/recommendations/{id} | ✅ Used |
| jobService.js | GET /matches/resume/{id} | ✅ Used |
| jobService.js | GET /matches/{r}/{j} | ✅ Used |
| jobService.js | POST /matches/generate/{r}/{j} | ✅ Used |
| userService.js | GET/PUT /user/profile | ✅ Used |
| **Not consumed by frontend** | /resume/{id}/parse | ❌ Unused |
| **Not consumed by frontend** | /resume/{id}/sections | ❌ Unused |
| **Not consumed by frontend** | /resume/{id}/extract | ❌ Unused |
| **Not consumed by frontend** | /resume/{id}/analyze | ❌ Unused |
| **Not consumed by frontend** | /resume/{id}/ats-score | ❌ Unused |
| **Not consumed by frontend** | /resume/{id}/ats-score/auto | ❌ Unused |
| **Not consumed by frontend** | All /resume/{id}/ats (ATS router) | ❌ Unused |
| **Not consumed by frontend** | POST /matches (create) | ❌ Unused |
| **Not consumed by frontend** | GET /matches/job/{id} | ❌ Unused |
| **Not consumed by frontend** | GET /profile (main.py) | ❌ Unused |

---

## 3. Confirmed Bugs

### P0 — App-Breaking

| # | Bug | Location | Evidence |
|---|-----|----------|----------|
| B-01 | `ats_score_repository.get_by_resume()` does not exist. Called in `generate_skill_match`. Crashes with `AttributeError` at runtime whenever a match is generated. | `backend/app/services/job_match.py:169` | Method not found in `ATSScoreRepository`; confirmed by grep. |
| B-02 | Rate limiting non-functional. `app.state.limiter = limiter` set but `app.add_middleware(SlowAPIMiddleware)` never called. `@limiter.limit` decorators raise `RuntimeError` at request time on the two routes that use them. | `backend/app/main.py` | No `SlowAPIMiddleware` import or `add_middleware` call in main.py. |

### P1 — Major Feature Broken

| # | Bug | Location | Evidence |
|---|-----|----------|----------|
| B-03 | Deleting a resume cascades to `ResumeAnalysis`, but `ATSScore.resume_analysis_id` FK has no `ondelete=CASCADE`. MySQL default is RESTRICT → `IntegrityError` if an ATSScore exists for that analysis. | `backend/app/models/ats_score.py` | FK defined without `ondelete`; `Resume.analysis` has `cascade="all, delete-orphan"`. DB unverified. |
| B-04 | 4 dead routes in job_match router. `get_job_matches_api` defined at lines 51–101 and 135–159. `get_job_recommendations_api` defined at lines 103–133 and 225–255. FastAPI registers only the first; duplicates are dead code. | `backend/app/routers/job_match.py` | Confirmed by line-by-line read. |
| B-05 | `processing_status` never set to `COMPLETED` anywhere in codebase. Resumes stay `PENDING` forever after upload. Dashboard displays this status. | `backend/app/services/resume.py` | Confirmed by grep: only `PENDING` assignment found, no `COMPLETED`. |

### P2 — Security / Data Integrity

| # | Bug | Location | Evidence |
|---|-----|----------|----------|
| B-06 | `ATSScoreResponse.resume_analysis_public_id` is always `""`. `ATSScore` model has no `resume_analysis` relationship. `hasattr(data, "resume_analysis")` returns False → field stays empty string in every API response. | `backend/app/schemas/ats_score.py`, `backend/app/models/ats_score.py` | Confirmed: no relationship defined on model. |
| B-07 | `GET /jobs/search` returns jobs of ALL statuses (DRAFT, CLOSED, OPEN). No status filter applied in `search_jobs`. DRAFT and CLOSED jobs leak publicly. | `backend/app/services/job.py` / `backend/app/repositories/job.py` | Confirmed by code read. |
| B-08 | `RateLimitExceeded` exception handler registered twice in `main.py` (lines ~52 and ~55). Second registration silently overwrites first. | `backend/app/main.py:52,55` | Confirmed by code read. |
| B-09 | `GET /profile` (main.py, line ~124) has no `response_model`, returns raw SQLAlchemy `User` ORM object. Serialization behavior is inconsistent; lazy-loaded relationships may cause unexpected output or errors. | `backend/app/main.py:124` | Confirmed: no response_model, returns ORM object directly. |

### P3 — Low / Cosmetic / Non-Idiomatic

| # | Issue | Location |
|---|-------|----------|
| B-10 | `@app.on_event("startup"/"shutdown")` is deprecated in modern FastAPI. Use lifespan context instead. | `backend/app/main.py` |
| B-11 | `min_match: float = Query(None, ...)` — non-idiomatic for Optional float in Pydantic v2 / FastAPI. Functional but should be `Optional[float] = Query(None, ...)`. | `backend/app/routers/job_match.py` |
| B-12 | `generate_skill_match`: if `semantic_score == 0`, expression `int(semantic_score) if semantic_score else None` evaluates to `None`, losing a valid 0 score. | `backend/app/services/job_match.py` |
| B-13 | `RecommendationEngine` uses the same `ats_score` (resume quality) for all jobs in a recommendation list. It is not job-specific — every recommendation has the same ATS component value. | `backend/app/ai/recommendation_engine.py` |
| B-14 | `update_resume` sets `processing_status=PENDING` but never triggers re-parsing or re-analysis. | `backend/app/services/resume.py` |
| B-15 | `create_match` (POST /matches) accepts arbitrary `match_score` from client with no 0–100 validation. | `backend/app/routers/job_match.py` |

---

## 4. Authorization Gaps

| Endpoint | Gap | Severity |
|----------|-----|----------|
| POST /resume/{id}/parse | Authenticated but no ownership check — any user can parse another user's resume | P2 |
| POST /resume/{id}/sections | Same as above | P2 |
| POST/GET/PUT /resume/{id}/ats (ATS router) | No ownership check | P2 |
| POST /matches | No ownership check on resume or job | P2 |
| GET /matches/resume/{id} | No ownership check | P2 |
| GET /matches/job/{id} | No ownership check | P2 |
| GET /matches/{r}/{j} | No ownership check | P2 |
| POST /matches/generate/{r}/{j} | No ownership check — user A can generate a match for user B's resume+job | P2 |

---

## 5. Architectural Issues

### Two Parallel Scoring Systems (Never Connected)
- **Deterministic ATS**: `ats_scores` table, populated via `/resume/{id}/ats-score` or `/ats-score/auto`. Requires manual trigger.
- **AI Analysis**: Groq result stored in `ai_analysis` JSON column of `ResumeAnalysis`. Triggered via `/resume/{id}/ai-analysis`.
- **Frontend ATSScore page** reads only `ai_analysis.overall_score` from Groq. The `ats_scores` table is completely ignored by the frontend. No `atsService` exists in frontend at all.
- **No automatic pipeline**: Upload → Parse → AI Analysis → ATS Score is NOT wired as one flow. Each step requires a separate manual API call.

### Duplicate Fields in JobMatch Model
- `match_score` (Integer, NOT NULL) and `overall_match` (nullable) both set to the same value in `generate_skill_match` (lines ~255, ~281).
- `experience_match_score` defined twice (lines 73, 118); `education_match_score` twice (86, 120); `project_match_score` twice (97, 122); `semantic_score` (102) vs `semantic_match_score` (124). SQLAlchemy last-definition wins.

### Stale Documentation
`docs/database.md` describes a schema that does not match the actual models:

| Item | docs/database.md says | Actual model |
|------|----------------------|--------------|
| ResumeAnalysis | Has overall_score, summary, strengths, weaknesses, recommendations, missing_skills, keyword_suggestions, experience_level, top_skills columns | None of these columns exist; results live only in `ai_analysis` JSON |
| ATSScore FK | `resume_public_id → resumes.public_id` | `resume_analysis_id → resume_analysis.id` |
| ATSScore columns | content_quality, skills_relevance, experience_depth, formatting_clarity | skills_score, education_score, experience_score, projects_score, format_score, section_score, keyword_score |
| ATSReport FK | `resume_public_id` | `resume_id → resumes.id` |
| Job model | Has requirements (NOT NULL), salary_range | Neither column exists |
| User model | Has user_public_id | Does not exist |
| Resume model | Has extracted_data | Does not exist |

### No External Job Feed
No third-party job API integration exists. Jobs are user-created only. There is no external job data source. Phase 2 job matching MVP has no real job feed.

---

## 6. Database Issues

| Issue | Severity | Details |
|-------|----------|---------|
| No Alembic | P1 | Schema changes via `run_migration.py`, `migration_add_user_columns.py`, `add_ai_analysis_column.sql`, and `Base.metadata.create_all`. No rollback capability. |
| Schema drift risk | P1 | `create_all` does not add columns added by separate migration scripts if models are already registered. Columns added via raw ALTER TABLE may be out of sync with the ORM model. |
| ATSScore FK missing ondelete | P1 | See Bug B-03. `ATSScore.resume_analysis_id` FK has no `ondelete=CASCADE`, causing potential delete failures. |
| No transactions for multi-step flows | P2 | Each repository method commits individually. If a multi-step service call fails midway, partial state is persisted with no rollback. |
| No indexes documented | P3 | No explicit index definitions found on frequently-queried foreign key columns (aside from PKs). Unverified against live DB. |
| Duplicate get_db | P3 | `app/dependencies.py` and `app/database/session.py` both define `get_db`. Identical implementations. |

---

## 7. Unused / Orphan Code

| Module / Method | Status | Reason |
|-----------------|--------|--------|
| `ATSReportService` + its repository | Orphan | No router mounts these endpoints |
| `resume_analysis_service` instance | Orphan | Routers use `ResumeService` directly |
| `JobMatchService.get_top_matches` | Unused | Not exposed via any route |
| `JobMatchService.match_job_to_resumes`, `match_resume_to_jobs` | Unused | Not exposed via any route |
| `SemanticMatcher.get_semantic_match_rating` | Unused | Not called anywhere |
| `SemanticMatcher.get_recommendation_summary` | Unused | Not called anywhere |
| `SemanticMatcher.clear_cache` | Used only in tests | |
| `RecommendationEngine.get_recommendation_summary` | Unused | |
| `OverallMatcher.get_score_breakdown`, `get_improvement_priorities` | Unused | |
| `SkillMatcher.get_skill_match_rating`, `get_skill_gap_analysis` | Unused | |
| `ExperienceMatcher.get_experience_match_rating`, `get_experience_insights` | Unused | |
| `EducationMatcher.get_education_match_rating`, `get_education_insights` | Unused | |
| `ProjectMatcher.get_project_match_rating`, `get_project_insights` | Unused | |
| `ResumeRepository.get_active_resumes` | Unused + broken | References `Resume.is_active` which does not exist → `OperationalError` if ever called |
| `ResumeRepository.get_by_filename` | Unused | |
| `JobRepository.get_by_status` | Unused | `get_open_jobs` uses inline filter |
| `get_current_admin` | Unused | No admin endpoints exist |
| `auth.py RegisterRequest`, `LoginRequest`, `UserLogin`, `Token` schemas | Unused | Auth router uses `schemas/user.py` versions |
| `app/ai/llm_service.py` | Empty (0 bytes) | Not imported anywhere |
| `app/ai/ats_analyzer.py` | Empty (0 bytes) | Not imported anywhere |
| `app/ai/job_matcher.py` | Empty (0 bytes) | Not imported anywhere |
| `app/middleware/` | Empty directory | No middleware files |
| `app/exceptions/handler.py: http_exception_handler` | Defined, not registered | FastAPI default handles HTTPException correctly |

---

## 8. Hardcoded / Configuration Issues

| Issue | Location | Severity |
|-------|----------|----------|
| `GROQ_MODEL` default hardcoded in `config.py` AND both AI modules' `get_groq_model()` | Multiple files | P3 |
| `GEMINI_API_KEY` config field present but unused; README/CHANGELOG/docstrings say "Gemini" but code uses Groq | `config.py`, `README.md`, `CHANGELOG.md`, `resume_analyzer.py` | P3 |
| CORS origins hardcoded in config default AND `.env` | `config.py` | P3 |
| `ALLOWED_CONTENT_TYPES`/`MAX_FILE_SIZE` duplicated in resume router and `fileConstants.js` (frontend) | Backend router + frontend constants | P3 |
| `app/ai/__init__.py` missing — `app/ai` treated as namespace package | `backend/app/ai/` | P3 |
| Sidebar.jsx footer reportedly says "GPT-4 Analysis Ready" — unverified | `frontend/src/components/Sidebar.jsx` | P3 (suspected) |

---

## 9. AI Module Status

| Module | File | Status |
|--------|------|--------|
| Resume Analyzer (Groq) | `app/ai/resume_analyzer.py` | Implemented (7656 bytes). Uses Groq. Docstring incorrectly says "Gemini". |
| Semantic Matcher | `app/ai/semantic_matcher.py` | Implemented. Duplicates Groq client init code from resume_analyzer. |
| LLM Service | `app/ai/llm_service.py` | **EMPTY (0 bytes)** |
| ATS Analyzer | `app/ai/ats_analyzer.py` | **EMPTY (0 bytes)** |
| Job Matcher AI | `app/ai/job_matcher.py` | **EMPTY (0 bytes)** |
| Skill Matcher | `app/matching/skill_matcher.py` | Implemented (deterministic) |
| Experience Matcher | `app/matching/experience_matcher.py` | Implemented (deterministic) |
| Education Matcher | `app/matching/education_matcher.py` | Implemented (deterministic) |
| Project Matcher | `app/matching/project_matcher.py` | Implemented (deterministic) |
| Overall Matcher | `app/matching/overall_matcher.py` | Implemented (deterministic) |
| ATS Scorers | `app/ats/` | Implemented (deterministic) |
| Recommendation Engine | `app/ai/recommendation_engine.py` | Implemented. Uses same ATS score for all jobs (design smell). |

---

## 10. Could Not Verify

- Live database schema (all FK behavior, actual columns present, index presence)
- Groq API connectivity and response parsing with real keys
- File storage behavior on Railway (relative `uploads/` path in container)
- Whether `generate_skill_match` (Bug B-01) has been patched in the live DB/deployed version
- Backend tests — no working Python environment with dependencies available during audit
- Whether `Sidebar.jsx` actually contains "GPT-4" text (reported by Cowork, not independently confirmed)
- `Profile.jsx` logout behavior (localStorage vs context — reported by Cowork Part 1)
- Actual Railway deployment logs and runtime errors