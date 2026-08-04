from pydantic import ConfigDict, model_validator

from app.schemas.common import BaseResponseSchema, BaseSchema


# ----------------------------
# ATS Score Base
# ----------------------------

class ATSScoreBase(BaseSchema):
    overall_score: float
    skills_score: float
    education_score: float
    experience_score: float
    projects_score: float
    format_score: float
    keyword_score: float
    missing_keywords: list[str] | None = None


# ----------------------------
# ATS Score Create
# ----------------------------

class ATSScoreCreate(ATSScoreBase):
    resume_analysis_id: int


# ----------------------------
# ATS Score Response
# ----------------------------

class ATSScoreResponse(
    BaseResponseSchema,
    ATSScoreBase,
):
    resume_analysis_public_id: str

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def resolve_ats_score_fields(cls, data: any) -> any:
        if isinstance(data, dict):
            return data

        resume_analysis_public_id_str = ""
        if hasattr(data, "resume_analysis") and data.resume_analysis:
            resume_analysis_public_id_str = str(data.resume_analysis.public_id)

        return {
            "public_id": data.public_id,
            "created_at": data.created_at,
            "updated_at": data.updated_at,
            "overall_score": data.overall_score,
            "skills_score": data.skills_score,
            "education_score": data.education_score,
            "experience_score": data.experience_score,
            "projects_score": data.projects_score,
            "format_score": data.format_score,
            "keyword_score": data.keyword_score,
            "missing_keywords": data.missing_keywords or [],
            "resume_analysis_public_id": resume_analysis_public_id_str,
        }
