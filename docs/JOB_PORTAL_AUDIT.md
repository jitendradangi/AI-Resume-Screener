# Job Portal – Existing Implementation Audit

**Date:** 2026-11-21
**Scope:** Job Portal section only (job CRUD, search, matching, recommendations) across `frontend/` (React) and `backend/` (FastAPI).
**Method:** Read-only code inspection. Model import verified by executing `app.models.job_match` with the project venv. No code, schema, or data was modified.

---

## 1. Frontend Inspection (React)

### Pages

| File | Role |
|---|---|
| `frontend/src/pages/jobs.jsx` | The only "Jobs" page. Despite the name it is a **job-match recommendations page**, not a job listing/browse page. It loads the user's resumes (`getMyResumes`), lets the user pick one, calls `GET /matches/recommendations/{resumeId}?top_n=10&min_match=50`, and renders recommendation cards. Lines 8–265. |
| `frontend/src/pages/MatchDetails.jsx` | Match detail page at route `/match/:resumePublicId/:jobPublicId` (`App.jsx:88`). Calls `GET /matches/{resume}/{job}` on mount; if no match exists it is *supposed* to offer a "Generate Match" button that calls `POST /matches/generate/{resume}/{job}`. Lines 15–45, 121–141. |
| `frontend/src/pages/dashboard.jsx` | Dashboard also calls `getJobRecommendations(latest.public_id, 5, 50)` (line 87) for a "best match" stat. |

### Services / API layer

- `frontend/src/services/api.js` (lines 1–7): single Axios instance, `baseURL = import.meta.env.VITE_API_BASE_URL`. `.env` contains `VITE_API_BASE_URL=http://localhost:8000`. **No request interceptor** — every caller manually attaches `Authorization: Bearer <token>` from `localStorage`.
- `frontend/src/services/jobService.js` exports:
  - `getJobs()` → `GET /jobs/` (auth) — **unused**
  - `getOpenJobs()` → `GET /jobs/open` (no auth) — **unused**
  - `searchJobs(params)` → `GET /jobs/search` (no auth) — **unused**
  - `getJobRecommendations(resumePublicId, topN, minMatch)` → `GET /matches/recommendations/{id}` — used by `jobs.jsx` and `dashboard.jsx`
  - `getResumeMatches(resumePublicId)` → `GET /matches/resume/{id}` — **unused**
  - `getMatch(resumePublicId, jobPublicId)` → `GET /matches/{r}/{j}` — used by `MatchDetails.jsx`
  - `generateMatch(resumePublicId, jobPublicId)` → `POST /matches/generate/{r}/{j}` — used by `MatchDetails.jsx`
  - `createJob(jobData)` → `POST /jobs/` — **unused**
  - `getJob(jobPublicId)` → `GET /jobs/{id}` — **unused**

### Routes / navigation

- `frontend/src/App.jsx`: `/jobs` (line 79) → `Jobs`; `/match/:resumePublicId/:jobPublicId` (line 88) → `MatchDetails`. Both wrapped in `ProtectedRoute`.
- `frontend/src/components/Sidebar.jsx:95` links to `/jobs` ("Jobs").
- **No routes exist** for job creation, job editing, job details/browse, or job search UI.

### States

- Loading: `jobs.jsx:85–93, 149–154`; `MatchDetails.jsx:66–74`. Present.
- Error: `jobs.jsx:141–146`; `MatchDetails.jsx:76–92, 115–119`. Present.
- Empty: `jobs.jsx:95–112` (no resumes), `jobs.jsx:250–259` (no recommendations). Present.

---

## 2. Backend Inspection (FastAPI)

### Routers

- `backend/app/routers/jobs.py` — prefix `/jobs`:
  - `POST /` create (auth) — lines 17–34
  - `GET /` list own jobs (auth) — lines 37–50
  - `GET /open` public open jobs — lines 53–59
  - `GET /search` public search by title/company/location — lines 62–75
  - `GET /{public_id}` own job only, 403 otherwise — lines 78–97
  - `PUT /{public_id}` update with ownership check — lines 100–124
  - `DELETE /{public_id}` delete with ownership check — lines 127–150
  - `POST /{public_id}/parse` parse job description — lines 153–167
- `backend/app/routers/job_match.py` — prefix `/matches`:
  - `POST ""` create match (client-supplied score) — lines 24–49
  - `GET /resume/{id}` — lines 51–75
  - `GET /job/{job_public_id}` — lines 77–101 **and duplicated verbatim at lines 135–159 (dead code)**
  - `GET /recommendations/{resume_public_id}` — lines 103–133 **and duplicated verbatim at lines 225–255 (dead code)**
  - `GET /{resume_public_id}/{job_public_id}` — lines 161–192
  - `POST /generate/{resume}/{job}` comprehensive match — lines 194–223

### Models / schema

- `backend/app/models/job.py` — `Job` table: `public_id` CHAR(36) UUID, `user_id` FK→users CASCADE, title/company/location/description, `required_skills` JSON, experience/education strings, five `parsed_*` columns, `employment_type`/`status` enums, timestamps. Relationships `user`, `job_matches` (cascade delete-orphan). Lines 21–101.
- `backend/app/models/job_match.py` — `JobMatch` table with `UniqueConstraint(resume_id, job_id)`, match score + extensive breakdown columns (skills, experience, education, projects, semantic, ATS). Lines 20–144.
  - **Duplicate column declarations (verified):** `experience_match_score` is declared at lines 73 and 118; `education_match_score` at lines 86 and 119; `project_match_score` at lines 97 and 121. Executing the model confirms SQLAlchemy silently keeps only the last binding — the first declarations are dead code (no crash, no duplicate DB columns).
- `backend/app/models/enums.py` — `JobStatus`: OPEN/CLOSED/DRAFT (default DRAFT, `job.py:74`); `EmploymentType`: FULL_TIME/PART_TIME/INTERNSHIP/CONTRACT/FREELANCE.
- `backend/app/schemas/job.py` — `JobBase`/`JobCreate`/`JobUpdate`/`JobResponse` with a `model_validator` that resolves `user_public_id` via the `user` relationship (lines 60–90).
- `backend/app/schemas/job_match.py` — `JobMatchResponse` exposes only: `public_id`, `created_at`, `match_score`, `recommendation`, `skills{matched,missing}`, `resume_public_id`, `job_public_id` (lines 40–77). `JobRecommendation` exposes `job_public_id, title, company, location, overall_match, match_level, component_scores, matched_skills, missing_skills` (lines 84–93).

### Services / repositories / matching

- `backend/app/services/job.py` — `JobService`: create/get/update/delete/list/search/`parse_job_description`. `job_service = JobService` (line 236, class not instance — routers call `job_service(db)` which works because it's the class).
- `backend/app/repositories/job.py` — queries; `get_open_jobs` filters `status == OPEN` (line 40); `search_by_*` use `ilike` **with no status filter** (lines 44–75).
- `backend/app/services/job_match.py` — `JobMatchService`: `create_match`, getters, `generate_skill_match` (full pipeline: SkillMatcher → ExperienceMatcher → EducationMatcher → ProjectMatcher → SemanticMatcher → OverallMatcher, lines 131–287), `match_resume_to_jobs` (289–324), `match_job_to_resumes` (326–365), `get_job_recommendations` (367–413).
- `backend/app/repositories/job_match.py` — `create_skill_match` persists all breakdown fields; `match_exists` enforces uniqueness.
- `backend/app/matching/` — skill/experience/education/project/overall matchers + `recommendation_engine.py` (returns dicts matching `JobRecommendation`, lines 102–119; semantic matching skipped for bulk recommendations, line 94).
- `backend/app/parsers/job_parser.py` — regex/keyword-based extraction of skills, experience, education, responsibilities, preferred skills.
- `backend/app/main.py` — both routers registered (lines 69, 71); `Base.metadata.create_all` at startup (line 37).

---

## 3. Frontend–Backend Integration

| Connection | Status |
|---|---|
| `jobs.jsx` → `GET /matches/recommendations/{id}` | **Works.** Response fields (`overall_match`, `match_level`, `component_scores`, `matched_skills`, `missing_skills`, `job_public_id`, `title`, `company`, `location`) exactly match `JobRecommendation` and the card UI. `min_match=50` is applied client-side as a query param — works. |
| `dashboard.jsx` → same endpoint | Works (same schema). |
| `MatchDetails.jsx` → `GET /matches/{r}/{j}` | **Schema mismatch + broken flow.** Backend `JobMatchResponse` has **no `component_scores`, no `match_level`, no `overall_match`** — the page renders `match.component_scores?.skills` etc., which is always `undefined` → all component bars show 0% (lines 239–322). `match.match_score`, `match.skills.matched/missing`, `match.recommendation` do exist. |
| `MatchDetails.jsx` → `POST /matches/generate/{r}/{j}` | Endpoint works, **but is unreachable in practice** — see bug B1 below. |
| `jobService.js` CRUD/search functions (`getJobs`, `getOpenJobs`, `searchJobs`, `createJob`, `getJob`, `getResumeMatches`) | Backend endpoints exist and schemas match, but **no UI calls them** — dead client code. |
| `POST /jobs/{id}/parse`, `match_resume_to_jobs`, `match_job_to_resumes`, `get_top_matches` | Backend implemented; **no route exposure for the batch methods and no frontend caller for parse** — dead/unused backend surface. |
| Auth | `get_current_user` on all mutating/protected endpoints; public endpoints (`/jobs/open`, `/jobs/search`) intentionally unauthenticated. Frontend attaches token manually per call — works but fragile (no interceptor, no 401 handling). |

---

## 4. Feature Completion Report

| Feature | Frontend Status | Backend Status | Integration Status | Missing Work |
|---|---|---|---|---|
| Job Listing | ❌ None (jobs.jsx is recommendations, not a job list) | ✅ `GET /jobs/`, `GET /jobs/open` | ⚠️ Endpoints exist; `getJobs`/`getOpenJobs` unused | Job browse/listing page + route |
| Job Details | ❌ None (`getJob` unused) | ✅ `GET /jobs/{public_id}` (owner-only) | ⚠️ Works only for owner; no public detail view | Job details page; decide public vs owner access |
| Job Search | ❌ None (`searchJobs` unused) | ⚠️ `GET /jobs/search` exists but OR-semantics + leaks drafts | ❌ Not connected | Search UI; fix filter semantics & status filtering |
| Filters | ❌ None | ⚠️ Only title/company/location params | ❌ | Filter UI (status, type, location, skills); backend param support |
| Job Creation | ❌ None (`createJob` unused) | ✅ `POST /jobs/` | ⚠️ API works; defaults to `DRAFT` so created jobs never appear in `/open` or recommendations | Creation form + status transition to OPEN |
| Job Update/Delete | ❌ None (no service functions at all) | ✅ `PUT`/`DELETE /jobs/{id}` with ownership checks | ❌ No client functions or UI | `updateJob`/`deleteJob` in jobService + edit/delete UI |
| Job Matching | ⚠️ Partial — MatchDetails page exists but see bugs | ✅ Full pipeline in `generate_skill_match` | ❌ Broken end-to-end (B1, B2) | Fix match retrieval/generation flow; expose component scores |
| Recommendations | ✅ Working (jobs.jsx + dashboard) | ✅ `GET /matches/recommendations/{id}` | ✅ Working | Persist matches optionally; pagination |

---

## 5. Final Findings

### Fully working
- **Job recommendations**: `GET /matches/recommendations/{resume_public_id}` → `RecommendationEngine` → `jobs.jsx`/`dashboard.jsx`. Schema match verified field-by-field.
- **Comprehensive match generation**: `POST /matches/generate/{r}/{j}` pipeline (skills, experience, education, projects, optional semantic, ATS) is complete in `services/job_match.py:131–287`.
- **Job CRUD backend**: create/read/update/delete with ownership enforcement in `routers/jobs.py` and `services/job.py`.
- **Job description parsing**: `JobParser` + `POST /jobs/{id}/parse` implemented.

### Partially implemented
- **Match details UI** (`MatchDetails.jsx`): renders score/skills/recommendation but component scores always show 0% because `JobMatchResponse` lacks `component_scores` (`schemas/job_match.py:40–77` vs `MatchDetails.jsx:239–322`).
- **Job search backend** (`services/job.py:160–183`): concatenates results per param — with multiple filters it returns jobs matching **ANY** criterion, not ALL (verified by code). Also no pagination.
- **Job listing**: backend returns all user jobs / all open jobs with no pagination, sorting, or status filtering on search.

### Missing features
- No job creation/editing/deletion UI anywhere in the frontend.
- No job browse/listing page, job details page, or search/filter UI.
- No way to set a job's `status` to `OPEN` from the UI — jobs created via API default to `DRAFT` (`models/job.py:74`) and are invisible to `/jobs/open` and recommendations. **The entire recommendations feature depends on jobs being OPEN, and nothing in the product can make a job OPEN.**
- `jobService.js` has no `updateJob`, `deleteJob`, or `parseJob` functions.
- No pagination on any job/match endpoint.

### Bugs and technical issues (verified)

- **B1 — MatchDetails "Generate Match" is unreachable.** `getMatch` 404s when no `JobMatch` row exists (recommendations are computed on-the-fly and never persisted — `services/job_match.py:367–413`). The catch sets `error`, and the early return at `MatchDetails.jsx:76` (`error && !match`) fires **before** the `{!match}` "Generate Match" panel at line 122 can render. Users always see the error screen; match details can never be generated via UI.
- **B2 — `component_scores` missing from `JobMatchResponse`.** Even when a match exists, `MatchDetails.jsx:239–322` reads `match.component_scores.*` which the API never returns → all five bars display 0%. `match_level`/`overall_match` also absent (page uses `match_score`, which exists).
- **B3 — Duplicate dead routes** in `routers/job_match.py`: `GET /job/{job_public_id}` defined twice (77–101 and 135–159); `GET /recommendations/{id}` twice (103–133 and 225–255). First registration wins; second is unreachable.
- **B4 — Duplicate column declarations** in `models/job_match.py` (lines 73/118, 86/119, 97/121). Verified harmless at runtime (SQLAlchemy keeps last binding; import test passed) but the first declarations are dead code.
- **B5 — `POST /jobs/{public_id}/parse` lacks ownership check** (`routers/jobs.py:153–167` → `services/job.py:185–233`). Any authenticated user can trigger parsing (and mutation of `parsed_*` fields) on **any** job by public_id. Update/delete correctly check `user_id`; parse does not.
- **B6 — Public search leaks non-public jobs.** `GET /jobs/search` and `GET /jobs/open`… `/open` is filtered, but `search_by_title/company/location` (`repositories/job.py:44–75`) have **no status filter** — `GET /jobs/search` unauthenticated returns DRAFT/CLOSED jobs of all users.
- **B7 — No ownership checks on match endpoints.** `GET /matches/resume/{id}`, `/job/{id}`, `/{r}/{j}`, `/recommendations/{id}`, and `POST /matches` never verify the resume/job belongs to `current_user` — any authenticated user can read/generate matches for any public_id.
- **B8 — Minor:** `getMatchLabel` defined but unused in `jobs.jsx:78–83`; `FaArrowLeft`, `FaBriefcase` unused imports in `jobs.jsx:4`; `match_resume_to_jobs`, `match_job_to_resumes`, `get_top_matches` service methods have no routes (dead backend code).

### Database/schema problems
- Duplicate column attribute names in `JobMatch` (B4) — cosmetic/dead code, but risks confusion.
- `match_score`, `overall_match`, `skill_match_score`, `experience/education/project_match_score`, `semantic_match_score`, `ats_score` are highly redundant — `match_score` duplicates `overall_match` (`services/job_match.py:255,281`).
- `JobMatch` has no `updated_at` column; `JobMatchResponse` validator falls back to `created_at` (`schemas/job_match.py:71`) — works but inconsistent with `Job`.
- `JSON` columns are MySQL-dialect-dependent (`sqlalchemy.dialects.mysql.CHAR` for public_id) — fine for MySQL/Railway, breaks on SQLite/Postgres.
- `create_all` at startup (`main.py:37`) — no Alembic migrations; schema drift risk.

### API integration problems
- Frontend↔backend contract mismatch on `JobMatchResponse` (B2).
- Unused service functions on both sides (dead code listed above).
- Manual `Authorization` header per call; no axios interceptor → no centralized 401/refresh handling.
- No API prefix (`/api`) — consistent between `.env` and routers, but worth noting for deployment.

### Recommended implementation order
1. **Fix B1** — either persist matches when generating recommendations, or make `MatchDetails` treat 404 as "no match" and show the Generate button (adjust the `error && !match` early return).
2. **Fix B2** — add `component_scores`, `match_level`, `overall_match` (or reuse `match_score`) to `JobMatchResponse` so MatchDetails renders real data.
3. **Fix B5/B6/B7** — add ownership checks to parse and match endpoints; add `status` filter to job search.
4. **Add job creation UI** with status control (set `OPEN`) — prerequisite for recommendations to have data.
5. **Add job listing/details/search UI** wiring the existing unused `jobService` functions; add `updateJob`/`deleteJob`/`parseJob` client functions.
6. **Cleanup** — remove duplicate routes (B3), duplicate columns (B4), unused service methods/imports.
7. **Add pagination** to list/search/recommendation endpoints.

---

*Audit complete. No implementation performed.*
