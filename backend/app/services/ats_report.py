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
        resume = resume_repository.get_by_public_id(self.db, resume_public_id)
        if not resume:
            raise ValueError("Resume not found.")

        if ats_report_repository.report_exists(self.db, resume.id):
            raise ValueError("ATS report already exists.")

        score_breakdown = report_data.pop("score_breakdown", None)
        if score_breakdown:
            if isinstance(score_breakdown, dict):
                report_data["skills_score"] = score_breakdown.get("skills_score")
                report_data["keyword_score"] = score_breakdown.get("keyword_score")
                report_data["experience_score"] = score_breakdown.get("experience_score")
                report_data["education_score"] = score_breakdown.get("education_score")
                report_data["formatting_score"] = score_breakdown.get("formatting_score")
                report_data["grammar_score"] = score_breakdown.get("grammar_score")
            else:
                report_data["skills_score"] = score_breakdown.skills_score
                report_data["keyword_score"] = score_breakdown.keyword_score
                report_data["experience_score"] = score_breakdown.experience_score
                report_data["education_score"] = score_breakdown.education_score
                report_data["formatting_score"] = score_breakdown.formatting_score
                report_data["grammar_score"] = score_breakdown.grammar_score

        ai_metadata = report_data.pop("ai_metadata", None)
        if ai_metadata:
            if isinstance(ai_metadata, dict):
                report_data["ai_model"] = ai_metadata.get("ai_model")
                report_data["analysis_version"] = ai_metadata.get("analysis_version")
                report_data["processing_time_ms"] = ai_metadata.get("processing_time_ms")
            else:
                report_data["ai_model"] = ai_metadata.ai_model
                report_data["analysis_version"] = ai_metadata.analysis_version
                report_data["processing_time_ms"] = ai_metadata.processing_time_ms

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
        resume = resume_repository.get_by_public_id(self.db, resume_public_id)
        if not resume:
            raise ValueError("Resume not found.")

        report = ats_report_repository.get_by_resume(self.db, resume.id)
        if not report:
            raise ValueError("ATS report not found.")

        score_breakdown = report_data.pop("score_breakdown", None)
        if score_breakdown is not None:
            if isinstance(score_breakdown, dict):
                report_data["skills_score"] = score_breakdown.get("skills_score")
                report_data["keyword_score"] = score_breakdown.get("keyword_score")
                report_data["experience_score"] = score_breakdown.get("experience_score")
                report_data["education_score"] = score_breakdown.get("education_score")
                report_data["formatting_score"] = score_breakdown.get("formatting_score")
                report_data["grammar_score"] = score_breakdown.get("grammar_score")
            else:
                report_data["skills_score"] = score_breakdown.skills_score
                report_data["keyword_score"] = score_breakdown.keyword_score
                report_data["experience_score"] = score_breakdown.experience_score
                report_data["education_score"] = score_breakdown.education_score
                report_data["formatting_score"] = score_breakdown.formatting_score
                report_data["grammar_score"] = score_breakdown.grammar_score

        ai_metadata = report_data.pop("ai_metadata", None)
        if ai_metadata is not None:
            if isinstance(ai_metadata, dict):
                report_data["ai_model"] = ai_metadata.get("ai_model")
                report_data["analysis_version"] = ai_metadata.get("analysis_version")
                report_data["processing_time_ms"] = ai_metadata.get("processing_time_ms")
            else:
                report_data["ai_model"] = ai_metadata.ai_model
                report_data["analysis_version"] = ai_metadata.analysis_version
                report_data["processing_time_ms"] = ai_metadata.processing_time_ms

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