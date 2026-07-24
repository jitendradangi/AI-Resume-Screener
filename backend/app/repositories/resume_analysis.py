from sqlalchemy.orm import Session

from app.models.resume_analysis import ResumeAnalysis
from app.repositories.base import BaseRepository


class ResumeAnalysisRepository(BaseRepository[ResumeAnalysis]):
    def __init__(self):
        super().__init__(ResumeAnalysis)

    def get_by_resume(
        self,
        db: Session,
        resume_id: int,
    ) -> ResumeAnalysis | None:
        return (
            db.query(self.model)
            .filter(self.model.resume_id == resume_id)
            .first()
        )

    def analysis_exists(
        self,
        db: Session,
        resume_id: int,
    ) -> bool:
        return (
            db.query(self.model)
            .filter(self.model.resume_id == resume_id)
            .first()
            is not None
        )

    def get_all_with_skill(
        self,
        db: Session,
        skill: str,
    ) -> list[ResumeAnalysis]:
        return (
            db.query(self.model)
            .filter(self.model.skills.contains([skill]))
            .all()
        )


resume_analysis_repository = ResumeAnalysisRepository()