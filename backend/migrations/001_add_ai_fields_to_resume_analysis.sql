-- Sprint 7 Task 5: AI resume analysis fields.
ALTER TABLE resume_analysis
    ADD COLUMN strengths JSON NULL,
    ADD COLUMN weaknesses JSON NULL,
    ADD COLUMN missing_skills JSON NULL,
    ADD COLUMN recommendations JSON NULL;
