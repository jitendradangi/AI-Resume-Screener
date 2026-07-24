from sqlalchemy.orm import Session

from app.models.resume_analysis import ResumeAnalysis
from app.repositories.resume import resume_repository
from app.repositories.resume_analysis import (
    resume_analysis_repository,
)
from app.services.base import BaseService


class ResumeAnalysisService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_analysis(
        self,
        resume_public_id: str,
        **analysis_data,
    ) -> ResumeAnalysis:

        resume = resume_repository.get_by_public_id(
            self.db,
            resume_public_id,
        )

        if not resume:
            raise ValueError("Resume not found.")

        if resume_analysis_repository.analysis_exists(
            self.db,
            resume.id,
        ):
            raise ValueError(
                "Resume analysis already exists."
            )

        return resume_analysis_repository.create(
            self.db,
            resume_id=resume.id,
            **analysis_data,
        )

    def get_analysis(
        self,
        resume_public_id: str,
    ) -> ResumeAnalysis | None:

        resume = resume_repository.get_by_public_id(
            self.db,
            resume_public_id,
        )

        if not resume:
            raise ValueError("Resume not found.")

        return resume_analysis_repository.get_by_resume(
            self.db,
            resume.id,
        )

    def update_analysis(
        self,
        resume_public_id: str,
        **analysis_data,
    ) -> ResumeAnalysis:

        resume = resume_repository.get_by_public_id(
            self.db,
            resume_public_id,
        )

        if not resume:
            raise ValueError("Resume not found.")

        analysis = (
            resume_analysis_repository.get_by_resume(
                self.db,
                resume.id,
            )
        )

        if not analysis:
            raise ValueError(
                "Resume analysis not found."
            )

        return resume_analysis_repository.update(
            self.db,
            analysis,
            **analysis_data,
        )


resume_analysis_service = ResumeAnalysisService