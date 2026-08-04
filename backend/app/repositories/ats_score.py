from sqlalchemy.orm import Session

from app.models.ats_score import ATSScore
from app.repositories.base import BaseRepository


class ATSScoreRepository(BaseRepository[ATSScore]):
    def __init__(self):
        super().__init__(ATSScore)

    def get_by_resume_analysis(
        self,
        db: Session,
        resume_analysis_id: int,
    ) -> ATSScore | None:
        return (
            db.query(self.model)
            .filter(self.model.resume_analysis_id == resume_analysis_id)
            .first()
        )

    def get_by_public_id(
        self,
        db: Session,
        public_id: str,
    ) -> ATSScore | None:
        return (
            db.query(self.model)
            .filter(self.model.public_id == public_id)
            .first()
        )

    def score_exists(
        self,
        db: Session,
        resume_analysis_id: int,
    ) -> bool:
        return (
            db.query(self.model)
            .filter(self.model.resume_analysis_id == resume_analysis_id)
            .first()
            is not None
        )

    def get_by_min_score(
        self,
        db: Session,
        min_score: float,
    ) -> list[ATSScore]:
        return (
            db.query(self.model)
            .filter(self.model.overall_score >= min_score)
            .all()
        )

    def get_top_scores(
        self,
        db: Session,
        limit: int = 10,
    ) -> list[ATSScore]:
        return (
            db.query(self.model)
            .order_by(self.model.overall_score.desc())
            .limit(limit)
            .all()
        )

    def create_score(
        self,
        db: Session,
        resume_analysis_id: int,
        overall_score: float,
        skills_score: float,
        education_score: float,
        experience_score: float,
        projects_score: float,
        format_score: float,
        section_score: float,
        keyword_score: float,
        missing_keywords: list | None = None,
        strengths: list | None = None,
        weaknesses: list | None = None,
        recommendations: list | None = None,
    ) -> ATSScore:
        return self.create(
            db,
            resume_analysis_id=resume_analysis_id,
            overall_score=overall_score,
            skills_score=skills_score,
            education_score=education_score,
            experience_score=experience_score,
            projects_score=projects_score,
            format_score=format_score,
            section_score=section_score,
            keyword_score=keyword_score,
            missing_keywords=missing_keywords,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
        )

    def update_score(
        self,
        db: Session,
        ats_score: ATSScore,
        overall_score: float | None = None,
        skills_score: float | None = None,
        education_score: float | None = None,
        experience_score: float | None = None,
        projects_score: float | None = None,
        format_score: float | None = None,
        section_score: float | None = None,
        keyword_score: float | None = None,
        missing_keywords: list | None = None,
        strengths: list | None = None,
        weaknesses: list | None = None,
        recommendations: list | None = None,
    ) -> ATSScore:
        update_kwargs = {}
        if overall_score is not None:
            update_kwargs["overall_score"] = overall_score
        if skills_score is not None:
            update_kwargs["skills_score"] = skills_score
        if education_score is not None:
            update_kwargs["education_score"] = education_score
        if experience_score is not None:
            update_kwargs["experience_score"] = experience_score
        if projects_score is not None:
            update_kwargs["projects_score"] = projects_score
        if format_score is not None:
            update_kwargs["format_score"] = format_score
        if section_score is not None:
            update_kwargs["section_score"] = section_score
        if keyword_score is not None:
            update_kwargs["keyword_score"] = keyword_score
        if missing_keywords is not None:
            update_kwargs["missing_keywords"] = missing_keywords
        if strengths is not None:
            update_kwargs["strengths"] = strengths
        if weaknesses is not None:
            update_kwargs["weaknesses"] = weaknesses
        if recommendations is not None:
            update_kwargs["recommendations"] = recommendations

        return self.update(db, ats_score, **update_kwargs)


ats_score_repository = ATSScoreRepository()
