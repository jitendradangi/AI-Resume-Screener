from pydantic import ConfigDict

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


class ATSReportResponse(
    BaseResponseSchema,
    ATSReportBase,
):
    resume_public_id: str

    model_config = ConfigDict(from_attributes=True)