from typing import Any
from pydantic import ConfigDict, model_validator

from app.schemas.common import BaseResponseSchema, BaseSchema


# ----------------------------
# Nested Schemas
# ----------------------------

class EducationSchema(BaseSchema):
    degree: str
    institution: str
    field_of_study: str | None = None
    grade: str | None = None
    start_year: int | None = None
    end_year: int | None = None


class ExperienceSchema(BaseSchema):
    company: str
    role: str
    location: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None


class ProjectSchema(BaseSchema):
    title: str
    description: str | None = None
    technologies: list[str] | None = None
    github_url: str | None = None
    live_url: str | None = None


class CertificationSchema(BaseSchema):
    name: str
    issuer: str | None = None
    issue_date: str | None = None


class LanguageSchema(BaseSchema):
    name: str
    proficiency: str | None = None

class SkillSchema(BaseSchema):
    name: str
    category: str | None = None
    proficiency: str | None = None


# ----------------------------
# Resume Analysis
# ----------------------------

class ResumeAnalysisBase(BaseSchema):
    summary: str | None = None

    skills: list[str] | None = None

    education: list[EducationSchema] | None = None

    experience: list[ExperienceSchema] | None = None

    projects: list[ProjectSchema] | None = None

    certifications: list[CertificationSchema] | None = None

    languages: list[LanguageSchema] | None = None


class ResumeAnalysisResponse(
    BaseResponseSchema,
    ResumeAnalysisBase,
):
    resume_public_id: str

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def resolve_analysis_fields(cls, data: any) -> any:
        if isinstance(data, dict):
            return data
            
        resume_public_id_str = ""
        if hasattr(data, "resume") and data.resume:
            resume_public_id_str = str(data.resume.public_id)
            
        return {
            "public_id": data.public_id,
            "created_at": data.created_at,
            "updated_at": data.updated_at,
            "summary": data.summary,
            "skills": data.skills or [],
            "education": data.education or [],
            "experience": data.experience or [],
            "projects": data.projects or [],
            "certifications": data.certifications or [],
            "languages": data.languages or [],
            "resume_public_id": resume_public_id_str,
        }


# ---------------------------------------------------------------------------
# Step 7 – AI Analysis response schema
# ---------------------------------------------------------------------------

class ScoreBreakdownSchema(BaseSchema):
    content_quality: int | None = None
    skills_relevance: int | None = None
    experience_depth: int | None = None
    formatting_clarity: int | None = None


class AIAnalysisResponse(BaseSchema):
    """Schema for the Gemini AI analysis result returned by POST /{id}/ai-analysis."""

    analysis_public_id: str
    resume_public_id: str

    overall_score: int | None = None
    score_breakdown: ScoreBreakdownSchema | None = None
    experience_level: str | None = None
    summary: str | None = None

    strengths: list[str] = []
    weaknesses: list[str] = []
    missing_skills: list[str] = []
    recommendations: list[str] = []
    keyword_suggestions: list[str] = []
    top_skills: list[str] = []

    # Raw Gemini dict — useful for debugging or future field additions
    raw: dict[str, Any] = {}

    @classmethod
    def from_service_result(cls, result: dict) -> "AIAnalysisResponse":
        """Build the response from the dict returned by ResumeService.run_ai_analysis()."""
        ai = result.get("ai_analysis", {})
        breakdown_raw = ai.get("score_breakdown")
        breakdown = (
            ScoreBreakdownSchema(**breakdown_raw) if isinstance(breakdown_raw, dict) else None
        )
        return cls(
            analysis_public_id=result["analysis_public_id"],
            resume_public_id=result["resume_public_id"],
            overall_score=ai.get("overall_score"),
            score_breakdown=breakdown,
            experience_level=ai.get("experience_level"),
            summary=ai.get("summary"),
            strengths=ai.get("strengths", []),
            weaknesses=ai.get("weaknesses", []),
            missing_skills=ai.get("missing_skills", []),
            recommendations=ai.get("recommendations", []),
            keyword_suggestions=ai.get("keyword_suggestions", []),
            top_skills=ai.get("top_skills", []),
            raw=ai,
        )