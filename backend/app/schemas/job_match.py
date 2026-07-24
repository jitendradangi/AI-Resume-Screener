from pydantic import ConfigDict

from app.schemas.common import BaseResponseSchema, BaseSchema


# ----------------------------
# Nested Schemas
# ----------------------------

class SkillMatchSchema(BaseSchema):
    matched: list[str] = []
    missing: list[str] = []

class MatchInsightsSchema(BaseSchema):
    matched_skill_count: int
    missing_skill_count: int
    total_required_skills: int


# ----------------------------
# Base
# ----------------------------

class JobMatchBase(BaseSchema):
    match_score: int

    recommendation: str | None = None

    skills: SkillMatchSchema


# ----------------------------
# Response
# ----------------------------

class JobMatchResponse(
    BaseResponseSchema,
    JobMatchBase,
):
    resume_public_id: str

    job_public_id: str

    model_config = ConfigDict(from_attributes=True)