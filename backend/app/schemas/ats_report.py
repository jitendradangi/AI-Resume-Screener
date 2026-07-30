from pydantic import ConfigDict, model_validator

from app.schemas.common import BaseResponseSchema, BaseSchema


# ----------------------------
# Nested Schemas
# ----------------------------

class ATSScoreBreakdown(BaseSchema):
    skills_score: int
    keyword_score: int
    experience_score: int
    education_score: int
    formatting_score: int
    grammar_score: int


class AIMetadata(BaseSchema):
    ai_model: str | None = None
    analysis_version: str | None = None
    processing_time_ms: int | None = None


# ----------------------------
# ATS Report
# ----------------------------

class ATSReportBase(BaseSchema):
    overall_score: int

    score_breakdown: ATSScoreBreakdown

    strengths: list[str] | None = None
    weaknesses: list[str] | None = None
    recommendations: list[str] | None = None
    missing_keywords: list[str] | None = None

    ai_metadata: AIMetadata | None = None


class ATSReportCreate(ATSReportBase):
    pass

class ATSReportResponse(
    BaseResponseSchema,
    ATSReportBase,
):
    resume_public_id: str

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def resolve_ats_fields(cls, data: any) -> any:
        if isinstance(data, dict):
            return data
            
        score_breakdown = {
            "skills_score": getattr(data, "skills_score", 0),
            "keyword_score": getattr(data, "keyword_score", 0),
            "experience_score": getattr(data, "experience_score", 0),
            "education_score": getattr(data, "education_score", 0),
            "formatting_score": getattr(data, "formatting_score", 0),
            "grammar_score": getattr(data, "grammar_score", 0),
        }
        
        ai_metadata = {
            "ai_model": getattr(data, "ai_model", None),
            "analysis_version": getattr(data, "analysis_version", None),
            "processing_time_ms": getattr(data, "processing_time_ms", None),
        }
        
        resume_public_id_str = ""
        if hasattr(data, "resume") and data.resume:
            resume_public_id_str = str(data.resume.public_id)
            
        return {
            "public_id": data.public_id,
            "created_at": data.created_at,
            "updated_at": getattr(data, "updated_at", data.created_at),
            "overall_score": data.overall_score,
            "score_breakdown": score_breakdown,
            "strengths": data.strengths or [],
            "weaknesses": data.weaknesses or [],
            "recommendations": data.recommendations or [],
            "missing_keywords": data.missing_keywords or [],
            "ai_metadata": ai_metadata,
            "resume_public_id": resume_public_id_str,
        }