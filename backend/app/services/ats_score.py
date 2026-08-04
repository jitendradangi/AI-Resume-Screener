from sqlalchemy.orm import Session

from app.models.ats_score import ATSScore
from app.repositories.ats_score import ats_score_repository
from app.repositories.resume_analysis import resume_analysis_repository
from app.services.base import BaseService


class ATSScoreService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def generate_score(
        self,
        resume_analysis_public_id: str,
        overall_score: float,
        skills_score: float,
        education_score: float,
        experience_score: float,
        projects_score: float,
        format_score: float,
        keyword_score: float,
        missing_keywords: list | None = None,
    ) -> ATSScore:
        resume_analysis = resume_analysis_repository.get_by_public_id(
            self.db,
            resume_analysis_public_id,
        )
        if not resume_analysis:
            raise ValueError("Resume analysis not found.")

        if ats_score_repository.score_exists(self.db, resume_analysis.id):
            raise ValueError("ATS score already exists for this resume analysis.")

        return ats_score_repository.create_score(
            self.db,
            resume_analysis_id=resume_analysis.id,
            overall_score=overall_score,
            skills_score=skills_score,
            education_score=education_score,
            experience_score=experience_score,
            projects_score=projects_score,
            format_score=format_score,
            keyword_score=keyword_score,
            missing_keywords=missing_keywords,
        )

    def get_score(
        self,
        public_id: str,
    ) -> ATSScore | None:
        score = ats_score_repository.get_by_public_id(self.db, public_id)
        if not score:
            raise ValueError("ATS score not found.")
        return score

    def get_score_by_resume_analysis(
        self,
        resume_analysis_public_id: str,
    ) -> ATSScore | None:
        resume_analysis = resume_analysis_repository.get_by_public_id(
            self.db,
            resume_analysis_public_id,
        )
        if not resume_analysis:
            raise ValueError("Resume analysis not found.")

        score = ats_score_repository.get_by_resume_analysis(
            self.db,
            resume_analysis.id,
        )
        if not score:
            raise ValueError("ATS score not found for this resume analysis.")
        return score

    def update_score(
        self,
        public_id: str,
        overall_score: float | None = None,
        skills_score: float | None = None,
        education_score: float | None = None,
        experience_score: float | None = None,
        projects_score: float | None = None,
        format_score: float | None = None,
        keyword_score: float | None = None,
        missing_keywords: list | None = None,
    ) -> ATSScore:
        score = ats_score_repository.get_by_public_id(self.db, public_id)
        if not score:
            raise ValueError("ATS score not found.")

        return ats_score_repository.update_score(
            self.db,
            score,
            overall_score=overall_score,
            skills_score=skills_score,
            education_score=education_score,
            experience_score=experience_score,
            projects_score=projects_score,
            format_score=format_score,
            keyword_score=keyword_score,
            missing_keywords=missing_keywords,
        )

    def delete_score(
        self,
        public_id: str,
    ) -> None:
        score = ats_score_repository.get_by_public_id(self.db, public_id)
        if not score:
            raise ValueError("ATS score not found.")

        ats_score_repository.delete(self.db, score)


ats_score_service = ATSScoreService
