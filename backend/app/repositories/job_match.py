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


job_match_repository = JobMatchRepository()