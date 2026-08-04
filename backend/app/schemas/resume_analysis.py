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

    strengths: list[str] | None = None

    weaknesses: list[str] | None = None

    missing_skills: list[str] | None = None

    recommendations: list[str] | None = None


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
            "strengths": data.strengths or [],
            "weaknesses": data.weaknesses or [],
            "missing_skills": data.missing_skills or [],
            "recommendations": data.recommendations or [],
            "resume_public_id": resume_public_id_str,
        }