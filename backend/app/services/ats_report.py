from sqlalchemy.orm import Session

from app.models.ats_report import ATSReport
from app.repositories.ats_report import ats_report_repository
from app.repositories.resume import resume_repository
from app.services.base import BaseService


class ATSReportService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_report(
        self,
        resume_public_id: str,
        **report_data,
    ) -> ATSReport:

        resume = resume_repository.get_by_public_id(
            self.db,
            resume_public_id,
        )

        if not resume:
            raise ValueError("Resume not found.")

        if ats_report_repository.report_exists(
            self.db,
            resume.id,
        ):
            raise ValueError(
                "ATS report already exists."
            )

        return ats_report_repository.create(
            self.db,
            resume_id=resume.id,
            **report_data,
        )

    def get_report(
        self,
        resume_public_id: str,
    ) -> ATSReport | None:

        resume = resume_repository.get_by_public_id(
            self.db,
            resume_public_id,
        )

        if not resume:
            raise ValueError("Resume not found.")

        return ats_report_repository.get_by_resume(
            self.db,
            resume.id,
        )

    def update_report(
        self,
        resume_public_id: str,
        **report_data,
    ) -> ATSReport:

        resume = resume_repository.get_by_public_id(
            self.db,
            resume_public_id,
        )

        if not resume:
            raise ValueError("Resume not found.")

        report = ats_report_repository.get_by_resume(
            self.db,
            resume.id,
        )

        if not report:
            raise ValueError(
                "ATS report not found."
            )

        return ats_report_repository.update(
            self.db,
            report,
            **report_data,
        )

    def get_top_reports(
        self,
        limit: int = 10,
    ) -> list[ATSReport]:

        return ats_report_repository.get_top_reports(
            self.db,
            limit,
        )


ats_report_service = ATSReportService