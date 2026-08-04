from pydantic import ConfigDict, Field, model_validator

from app.schemas.common import BaseResponseSchema, BaseSchema


class ATSScoreBreakdown(BaseSchema):
    skills_score: int = Field(ge=0, le=100)
    keyword_score: int = Field(ge=0, le=100)
    experience_score: int = Field(ge=0, le=100)
    education_score: int = Field(ge=0, le=100)
    formatting_score: int = Field(ge=0, le=100)
    grammar_score: int = Field(ge=0, le=100)


class ATSScoreBase(BaseSchema):
    overall_score: int = Field(ge=0, le=100)
    score_breakdown: ATSScoreBreakdown

    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)

    ai_model: str | None = None
    analysis_version: str | None = None
    processing_time_ms: int | None = Field(default=None, ge=0)


class ATSScoreCreate(ATSScoreBase):
    pass


class ATSScoreResponse(
    BaseResponseSchema,
    ATSScoreBase,
):
    resume_public_id: str

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def resolve_ats_score_fields(cls, data: object) -> object:
        if isinstance(data, dict):
            return data

        score_breakdown = {
            "skills_score": data.skills_score or 0,
            "keyword_score": data.keyword_score or 0,
            "experience_score": data.experience_score or 0,
            "education_score": data.education_score or 0,
            "formatting_score": data.formatting_score or 0,
            "grammar_score": data.grammar_score or 0,
        }

        resume_public_id = ""
        if data.resume:
            resume_public_id = str(data.resume.public_id)

        return {
            "public_id": data.public_id,
            "created_at": data.created_at,
            "updated_at": data.created_at,
            "overall_score": data.overall_score,
            "score_breakdown": score_breakdown,
            "strengths": data.strengths or [],
            "weaknesses": data.weaknesses or [],
            "recommendations": data.recommendations or [],
            "missing_keywords": data.missing_keywords or [],
            "ai_model": data.ai_model,
            "analysis_version": data.analysis_version,
            "processing_time_ms": data.processing_time_ms,
            "resume_public_id": resume_public_id,
        }
