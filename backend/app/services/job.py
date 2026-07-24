from sqlalchemy.orm import Session

from app.models.job import Job
from app.repositories.job import job_repository
from app.repositories.user import user_repository
from app.services.base import BaseService


class JobService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_job(
        self,
        creator_public_id: str,
        **job_data,
    ) -> Job:

        creator = user_repository.get_by_public_id(
            self.db,
            creator_public_id,
        )

        if not creator:
            raise ValueError("Creator not found.")

        return job_repository.create(
            self.db,
            created_by=creator.id,
            **job_data,
        )

    def get_job(
        self,
        public_id: str,
    ) -> Job | None:

        return job_repository.get_by_public_id(
            self.db,
            public_id,
        )

    def update_job(
        self,
        public_id: str,
        **job_data,
    ) -> Job:

        job = job_repository.get_by_public_id(
            self.db,
            public_id,
        )

        if not job:
            raise ValueError("Job not found.")

        return job_repository.update(
            self.db,
            job,
            **job_data,
        )

    def delete_job(
        self,
        public_id: str,
    ) -> None:

        job = job_repository.get_by_public_id(
            self.db,
            public_id,
        )

        if not job:
            raise ValueError("Job not found.")

        job_repository.delete(
            self.db,
            job,
        )

    def get_all_jobs(self) -> list[Job]:
        return job_repository.get_all(self.db)

    def get_active_jobs(self) -> list[Job]:
        return job_repository.get_active_jobs(
            self.db,
        )

    def get_jobs_by_company(
        self,
        company: str,
    ) -> list[Job]:
        return job_repository.get_by_company(
            self.db,
            company,
        )

    def get_jobs_by_location(
        self,
        location: str,
    ) -> list[Job]:
        return job_repository.get_by_location(
            self.db,
            location,
        )

    def search_jobs(
        self,
        keyword: str,
    ) -> list[Job]:
        return job_repository.search_by_title(
            self.db,
            keyword,
        )


job_service = JobService