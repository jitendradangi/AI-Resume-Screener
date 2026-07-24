from pydantic import ConfigDict

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