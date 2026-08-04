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

    def create_analysis(
        self,
        db: Session,
        resume_id: int,
        raw_text: str,
        parsed_data: dict | None = None,
        summary: str | None = None,
        skills: list | None = None,
        education: list | None = None,
        experience: list | None = None,
        projects: list | None = None,
        certifications: list | None = None,
        languages: list | None = None,
        ai_analysis: dict | None = None,
    ) -> ResumeAnalysis:
        return self.create(
            db,
            resume_id=resume_id,
            raw_text=raw_text,
            parsed_data=parsed_data,
            summary=summary,
            skills=skills,
            education=education,
            experience=experience,
            projects=projects,
            certifications=certifications,
            languages=languages,
            ai_analysis=ai_analysis,
        )

    def update_analysis(
        self,
        db: Session,
        analysis: ResumeAnalysis,
        raw_text: str | None = None,
        parsed_data: dict | None = None,
        summary: str | None = None,
        skills: list | None = None,
        education: list | None = None,
        experience: list | None = None,
        projects: list | None = None,
        certifications: list | None = None,
        languages: list | None = None,
        ai_analysis: dict | None = None,
    ) -> ResumeAnalysis:
        update_kwargs = {}
        if raw_text is not None:
            update_kwargs["raw_text"] = raw_text
        if parsed_data is not None:
            update_kwargs["parsed_data"] = parsed_data
        if summary is not None:
            update_kwargs["summary"] = summary
        if skills is not None:
            update_kwargs["skills"] = skills
        if education is not None:
            update_kwargs["education"] = education
        if experience is not None:
            update_kwargs["experience"] = experience
        if projects is not None:
            update_kwargs["projects"] = projects
        if certifications is not None:
            update_kwargs["certifications"] = certifications
        if languages is not None:
            update_kwargs["languages"] = languages
        if ai_analysis is not None:
            update_kwargs["ai_analysis"] = ai_analysis

        return self.update(db, analysis, **update_kwargs)


resume_analysis_repository = ResumeAnalysisRepository()