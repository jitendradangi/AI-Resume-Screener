# Audit Notes, Part 1 (reported by Cowork, line numbers from its reads)

## Stack
- Backend: FastAPI, SQLAlchemy, MySQL, Pydantic v2, JWT, bcrypt, slowapi, groq
- Frontend: React 19, Vite, Tailwind 4, React Router 7, Axios
- Tests: 1 file (test_groq_config.py, 7 tests, Groq config only); 2 ad-hoc scripts
  (test_profile_api.py, test_user_service.py, hardcoded email); backend/test is a 0-byte FILE
- requirements.txt fully pinned. backend/.env exists and is gitignored.

## Critical / High
1. Rate limiting likely non-functional: app.state.limiter set, but
   app.add_middleware(SlowAPIMiddleware) is missing (main.py).
2. Empty AI modules (0 bytes, imported nowhere): app/ai/llm_service.py,
   ats_analyzer.py, job_matcher.py. Only resume_analyzer.py has content.
   semantic_matcher.py duplicates the Groq client code.
3. Two parallel scoring systems: frontend ATSScore page shows the Groq overall_score
   (from ai_analysis); the deterministic ats_scores table is ignored by that page.
4. No automatic pipeline upload -> parse -> analyze -> ATS score.
   create_ats_score / create_ats_score_auto need manual input.
5. Duplicate routes in job_match router: get_job_matches_api (lines 51-101 and 135-159),
   get_job_recommendations_api (103-133 and 225-255). FastAPI uses the first registered;
   4 of 8 route definitions are dead.
6. Schema vs docs mismatch (docs/database.md is stale):
   - ResumeAnalysis has no overall_score/summary/strengths/etc. columns; results live only
     in the ai_analysis JSON column
   - ATSScore FK is resume_analysis_id (docs say resume_public_id); no relationship to Resume
   - ATSReport FK is resume_id (docs say resume_public_id)
   - Job has no requirements/salary_range; User has no user_public_id; Resume has no extracted_data
7. No Alembic. Schema changes via run_migration.py, migration_add_user_columns.py and
   Base.metadata.create_all at startup.
8. Frontend VITE_API_BASE_URL hardcoded to http://localhost:8000 (no env switching).
9. main.py /profile (line ~124): no response_model, returns raw User ORM object, duplicates
   /user/profile. Serialization failure suspected, NOT verified.

## Medium / Low
- Docs say "Google Gemini" (README, CHANGELOG, resume_analyzer.py docstring); code uses Groq.
  GEMINI_API_KEY config field unused. Sidebar.jsx says "GPT-4 Analysis Ready".
- RateLimitExceeded handler registered twice (main.py ~52, 55); @app.on_event deprecated.
- app/middleware/ is empty; app/ai/__init__.py missing.
- JobMatch has duplicate fields match_score and overall_match (set to same value).
- SemanticMatcher failure swallowed by bare `except Exception: pass` in generate_skill_match.
- update_resume sets processing_status=PENDING but never triggers reprocessing.
- Dashboard ATS card only shows data after ai-analysis is run (reads ai_analysis.overall_score).
- Duplicate frontend routes /ats-score/:public_id and /ats-score.
- Profile.jsx logout uses localStorage.removeItem("token") instead of context logout().
- Duplicated constants: ALLOWED_CONTENT_TYPES/MAX_FILE_SIZE (router and fileConstants.js);
  CORS origins hardcoded; GROQ_MODEL default hardcoded in config and both AI modules.
- Query(None) with float annotation on min_match: non-idiomatic, NEEDS VERIFICATION.
- get_current_admin defined, never used.
- No external job feed. Jobs are user-created only.

## Unused code candidates (Cowork says references checked)
ResumeRepository.get_active_resumes/get_by_filename; JobRepository.get_by_status;
ATSReportService + repository (no router); resume_analysis_service instance;
JobMatchService.get_top_matches/match_job_to_resumes; SemanticMatcher.clear_cache,
get_semantic_match_rating, get_skill_gap_analysis, get_recommendation_summary.

## Not covered in this pass (do in later sessions)
Auth details (JWT expiry, ownership checks), upload validation and storage, PDF/DOCX
extraction, section identification. No tests were run, and Groq/DB were not verified live.