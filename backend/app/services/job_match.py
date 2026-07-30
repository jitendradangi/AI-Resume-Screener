from sqlalchemy.orm import Session

from app.models.job_match import JobMatch
from app.repositories.job import job_repository
from app.repositories.job_match import job_match_repository
from app.repositories.resume import resume_repository
from app.services.base import BaseService


class JobMatchService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_match(
        self,
        resume_public_id: str,
        job_public_id: str,
        **match_data,
    ) -> JobMatch:
        resume = resume_repository.get_by_public_id(self.db, resume_public_id)
        if not resume:
            raise ValueError("Resume not found.")

        job = job_repository.get_by_public_id(self.db, job_public_id)
        if not job:
            raise ValueError("Job not found.")

        if job_match_repository.match_exists(self.db, resume.id, job.id):
            raise ValueError("Match already exists.")

        skills = match_data.pop("skills", None)
        if skills:
            if isinstance(skills, dict):
                match_data["matched_skills"] = skills.get("matched", [])
                match_data["missing_skills"] = skills.get("missing", [])
            else:
                match_data["matched_skills"] = skills.matched
                match_data["missing_skills"] = skills.missing

        return job_match_repository.create(
            self.db,
            resume_id=resume.id,
            job_id=job.id,
            **match_data,
        )

    def get_match(
        self,
        resume_public_id: str,
        job_public_id: str,
    ) -> JobMatch | None:

        resume = resume_repository.get_by_public_id(
            self.db,
            resume_public_id,
        )

        if not resume:
            raise ValueError("Resume not found.")

        job = job_repository.get_by_public_id(
            self.db,
            job_public_id,
        )

        if not job:
            raise ValueError("Job not found.")

        return job_match_repository.get_resume_job_match(
            self.db,
            resume.id,
            job.id,
        )

    def get_resume_matches(
        self,
        resume_public_id: str,
    ) -> list[JobMatch]:

        resume = resume_repository.get_by_public_id(
            self.db,
            resume_public_id,
        )

        if not resume:
            raise ValueError("Resume not found.")

        return job_match_repository.get_by_resume(
            self.db,
            resume.id,
        )

    def get_job_matches(
        self,
        job_public_id: str,
    ) -> list[JobMatch]:

        job = job_repository.get_by_public_id(
            self.db,
            job_public_id,
        )

        if not job:
            raise ValueError("Job not found.")

        return job_match_repository.get_by_job(
            self.db,
            job.id,
        )

    def get_top_matches(
        self,
        limit: int = 10,
    ) -> list[JobMatch]:

        return job_match_repository.get_top_matches(
            self.db,
            limit,
        )


job_match_service = JobMatchService