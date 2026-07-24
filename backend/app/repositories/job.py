from sqlalchemy.orm import Session

from app.models.enums import JobStatus
from app.models.job import Job
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository[Job]):
    def __init__(self):
        super().__init__(Job)

    def get_active_jobs(
        self,
        db: Session,
    ) -> list[Job]:
        return (
            db.query(self.model)
            .filter(self.model.is_active == True)
            .all()
        )

    def get_by_status(
        self,
        db: Session,
        status: JobStatus,
    ) -> list[Job]:
        return (
            db.query(self.model)
            .filter(self.model.status == status)
            .all()
        )

    def get_by_company(
        self,
        db: Session,
        company: str,
    ) -> list[Job]:
        return (
            db.query(self.model)
            .filter(self.model.company == company)
            .all()
        )

    def get_by_location(
        self,
        db: Session,
        location: str,
    ) -> list[Job]:
        return (
            db.query(self.model)
            .filter(self.model.location == location)
            .all()
        )

    def get_by_creator(
        self,
        db: Session,
        user_id: int,
    ) -> list[Job]:
        return (
            db.query(self.model)
            .filter(self.model.created_by == user_id)
            .all()
        )

    def search_by_title(
        self,
        db: Session,
        keyword: str,
    ) -> list[Job]:
        return (
            db.query(self.model)
            .filter(self.model.title.ilike(f"%{keyword}%"))
            .all()
        )

    def get_by_skill(
        self,
        db: Session,
        skill: str,
    ) -> list[Job]:
        return (
            db.query(self.model)
            .filter(self.model.required_skills.contains([skill]))
            .all()
        )


job_repository = JobRepository()