from sqlalchemy.orm import Session

from app.ai.resume_analyzer import (
    AIAnalysisError,
    ResumeAnalyzer,
)
from app.models.resume_analysis import ResumeAnalysis
from app.parsers.resume_parser import ResumeParser
from app.parsers.text_extractor import TextExtractor
from app.repositories.resume import resume_repository
from app.repositories.resume_analysis import (
    resume_analysis_repository,
)
from app.services.base import BaseService


class ResumeAnalysisService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def run_ai_analysis(
        self,
        resume_public_id: str,
        user_id: int | None = None,
        analyzer: ResumeAnalyzer | None = None,
    ) -> ResumeAnalysis:

        resume = resume_repository.get_by_public_id(
            self.db,
            resume_public_id,
        )

        if not resume:
            raise ValueError("Resume not found.")

        if user_id is not None and resume.user_id != user_id:
            raise PermissionError(
                "Unauthorized to analyse this resume."
            )

        analysis = (
            resume_analysis_repository.get_by_resume(
                self.db,
                resume.id,
            )
        )

        # Reuse the already parsed resume instead of parsing again.
        if analysis and analysis.raw_text:
            resume_text = analysis.raw_text
            extracted_data = analysis.parsed_data or {}
        else:
            try:
                resume_text = TextExtractor.extract(
                    resume.filepath
                )
            except (ValueError, OSError) as exc:
                raise AIAnalysisError(
                    f"Could not read resume file: {exc}"
                ) from exc

            extracted_data = ResumeParser.parse(resume_text)

        ai_result = (
            analyzer or ResumeAnalyzer()
        ).analyze_resume(
            resume_text,
            extracted_data,
        )

        analysis_data = {
            "raw_text": resume_text,
            "parsed_data": extracted_data,
            "skills": extracted_data.get("skills") or [],
            "education": extracted_data.get("education") or [],
            "experience": extracted_data.get("experience") or [],
            "projects": extracted_data.get("projects") or [],
            "certifications": extracted_data.get(
                "certifications"
            )
            or [],
            "languages": extracted_data.get("languages") or [],
            "summary": ai_result["summary"],
            "strengths": ai_result["strengths"],
            "weaknesses": ai_result["weaknesses"],
            "missing_skills": ai_result["missing_skills"],
            "recommendations": ai_result["recommendations"],
        }

        if analysis:
            return resume_analysis_repository.update(
                self.db,
                analysis,
                **analysis_data,
            )

        return resume_analysis_repository.create(
            self.db,
            resume_id=resume.id,
            **analysis_data,
        )

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