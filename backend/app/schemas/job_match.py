from pydantic import ConfigDict, model_validator

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

class JobMatchCreate(JobMatchBase):
    resume_public_id: str
    job_public_id: str

class JobMatchResponse(
    BaseResponseSchema,
    JobMatchBase,
):
    resume_public_id: str
    job_public_id: str

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def resolve_job_match_fields(cls, data: any) -> any:
        if isinstance(data, dict):
            return data
            
        skills = {
            "matched": getattr(data, "matched_skills", []) or [],
            "missing": getattr(data, "missing_skills", []) or [],
        }
        
        resume_public_id_str = ""
        if hasattr(data, "resume") and data.resume:
            resume_public_id_str = str(data.resume.public_id)
            
        job_public_id_str = ""
        if hasattr(data, "job") and data.job:
            job_public_id_str = str(data.job.public_id)
            
        return {
            "public_id": data.public_id,
            "created_at": data.created_at,
            "updated_at": getattr(data, "updated_at", data.created_at),
            "match_score": data.match_score,
            "recommendation": data.recommendation,
            "skills": skills,
            "resume_public_id": resume_public_id_str,
            "job_public_id": job_public_id_str,
        }