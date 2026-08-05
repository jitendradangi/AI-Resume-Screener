from sqlalchemy.orm import Session

from app.models.job_match import JobMatch
from app.repositories.base import BaseRepository


class JobMatchRepository(BaseRepository[JobMatch]):
    def __init__(self):
        super().__init__(JobMatch)

    def get_by_resume(
        self,
        db: Session,
        resume_id: int,
    ) -> list[JobMatch]:
        return (
            db.query(self.model)
            .filter(self.model.resume_id == resume_id)
            .order_by(self.model.match_score.desc())
            .all()
        )

    def get_by_job(
        self,
        db: Session,
        job_id: int,
    ) -> list[JobMatch]:
        return (
            db.query(self.model)
            .filter(self.model.job_id == job_id)
            .order_by(self.model.match_score.desc())
            .all()
        )

    def get_resume_job_match(
        self,
        db: Session,
        resume_id: int,
        job_id: int,
    ) -> JobMatch | None:
        return (
            db.query(self.model)
            .filter(
                self.model.resume_id == resume_id,
                self.model.job_id == job_id,
            )
            .first()
        )

    def get_top_matches(
        self,
        db: Session,
        limit: int = 10,
    ) -> list[JobMatch]:
        return (
            db.query(self.model)
            .order_by(self.model.match_score.desc())
            .limit(limit)
            .all()
        )

    def match_exists(
        self,
        db: Session,
        resume_id: int,
        job_id: int,
    ) -> bool:
        return (
            db.query(self.model)
            .filter(
                self.model.resume_id == resume_id,
                self.model.job_id == job_id,
            )
            .first()
            is not None
        )

    def create_skill_match(
        self,
        db: Session,
        resume_id: int,
        job_id: int,
        match_score: int,
        matched_skills: list,
        missing_skills: list,
        matched_preferred_skills: list | None = None,
        extra_skills: list | None = None,
        skill_match_breakdown: dict | None = None,
        candidate_years: int | None = None,
        required_min_years: int | None = None,
        required_max_years: int | None = None,
        experience_match_score: int | None = None,
        experience_match_breakdown: dict | None = None,
        candidate_degree: str | None = None,
        candidate_level: int | None = None,
        required_degree: str | None = None,
        required_level: int | None = None,
        education_match_score: int | None = None,
        education_match_breakdown: dict | None = None,
        has_projects: int | None = None,
        relevant_projects_count: int | None = None,
        total_projects_count: int | None = None,
        project_match_score: int | None = None,
        project_match_breakdown: dict | None = None,
        semantic_score: int | None = None,
        semantic_strengths: list | None = None,
        semantic_weaknesses: list | None = None,
        semantic_reason: str | None = None,
        overall_match: int | None = None,
        match_level: str | None = None,
        skill_match_score: int | None = None,
        experience_match_score: int | None = None,
        education_match_score: int | None = None,
        project_match_score: int | None = None,
        semantic_match_score: int | None = None,
        ats_score: int | None = None,
        recommendation: str | None = None,
    ) -> JobMatch:
        """Create a skill-based match with all detailed analysis data."""
        return self.create(
            db,
            resume_id=resume_id,
            job_id=job_id,
            match_score=match_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            matched_preferred_skills=matched_preferred_skills,
            extra_skills=extra_skills,
            skill_match_breakdown=skill_match_breakdown,
            candidate_years=candidate_years,
            required_min_years=required_min_years,
            required_max_years=required_max_years,
            experience_match_score=experience_match_score,
            experience_match_breakdown=experience_match_breakdown,
            candidate_degree=candidate_degree,
            candidate_level=candidate_level,
            required_degree=required_degree,
            required_level=required_level,
            education_match_score=education_match_score,
            education_match_breakdown=education_match_breakdown,
            has_projects=bool(has_projects) if has_projects is not None else None,
            relevant_projects_count=relevant_projects_count,
            total_projects_count=total_projects_count,
            project_match_score=project_match_score,
            project_match_breakdown=project_match_breakdown,
            semantic_score=semantic_score,
            semantic_strengths=semantic_strengths,
            semantic_weaknesses=semantic_weaknesses,
            semantic_reason=semantic_reason,
            overall_match=overall_match,
            match_level=match_level,
            skill_match_score=skill_match_score,
            experience_match_score=experience_match_score,
            education_match_score=education_match_score,
            project_match_score=project_match_score,
            semantic_match_score=semantic_match_score,
            ats_score=ats_score,
            recommendation=recommendation,
        )


job_match_repository = JobMatchRepository()