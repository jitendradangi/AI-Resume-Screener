from sqlalchemy.orm import Session

from app.models.ats_report import ATSReport
from app.repositories.base import BaseRepository


class ATSReportRepository(BaseRepository[ATSReport]):
    def __init__(self):
        super().__init__(ATSReport)

    def get_by_resume(
        self,
        db: Session,
        resume_id: int,
    ) -> ATSReport | None:
        return (
            db.query(self.model)
            .filter(self.model.resume_id == resume_id)
            .first()
        )

    def report_exists(
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

    def get_by_min_score(
        self,
        db: Session,
        min_score: int,
    ) -> list[ATSReport]:
        return (
            db.query(self.model)
            .filter(self.model.overall_score >= min_score)
            .all()
        )

    def get_top_reports(
        self,
        db: Session,
        limit: int = 10,
    ) -> list[ATSReport]:
        return (
            db.query(self.model)
            .order_by(self.model.overall_score.desc())
            .limit(limit)
            .all()
        )


ats_report_repository = ATSReportRepository()