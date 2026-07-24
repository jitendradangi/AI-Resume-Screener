from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.repositories.base import BaseRepository


class ResumeRepository(BaseRepository[Resume]):
    def __init__(self):
        super().__init__(Resume)

    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[Resume]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .all()
        )

    def get_latest_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> Resume | None:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .first()
        )

    def get_by_filename(
        self,
        db: Session,
        filename: str,
    ) -> Resume | None:
        return (
            db.query(self.model)
            .filter(self.model.filename == filename)
            .first()
        )

    def get_active_resumes(
        self,
        db: Session,
    ) -> list[Resume]:
        return (
            db.query(self.model)
            .filter(self.model.is_active == True)
            .all()
        )


resume_repository = ResumeRepository()