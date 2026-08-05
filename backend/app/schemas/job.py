from datetime import datetime

from pydantic import ConfigDict, model_validator

from app.models.enums import EmploymentType, JobStatus
from app.schemas.common import BaseResponseSchema, BaseSchema


class JobBase(BaseSchema):
    """Common job fields."""

    title: str
    company: str
    location: str | None = None
    description: str | None = None
    required_skills: list[str] | None = None
    experience: str | None = None
    education: str | None = None
    employment_type: EmploymentType | None = None
    salary: str | None = None
    status: JobStatus = JobStatus.DRAFT


class JobCreate(JobBase):
    """Schema for creating a job."""

    pass


class JobUpdate(BaseSchema):
    """Schema for updating a job."""

    title: str | None = None
    company: str | None = None
    location: str | None = None
    description: str | None = None
    required_skills: list[str] | None = None
    experience: str | None = None
    education: str | None = None
    employment_type: EmploymentType | None = None
    salary: str | None = None
    status: JobStatus | None = None


class JobResponse(
    BaseResponseSchema,
    JobBase,
):
    """Job details returned to clients."""

    user_public_id: str
    parsed_required_skills: list[str] | None = None
    parsed_required_experience: str | None = None
    parsed_required_education: str | None = None
    parsed_responsibilities: list[str] | None = None
    parsed_preferred_skills: list[str] | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def resolve_job_fields(cls, data: any) -> any:
        if isinstance(data, dict):
            return data

        user_public_id_str = ""
        if hasattr(data, "user") and data.user:
            user_public_id_str = str(data.user.public_id)

        return {
            "public_id": data.public_id,
            "created_at": data.created_at,
            "updated_at": data.updated_at,
            "title": data.title,
            "company": data.company,
            "location": data.location,
            "description": data.description,
            "required_skills": data.required_skills or [],
            "experience": data.experience,
            "education": data.education,
            "employment_type": data.employment_type,
            "salary": data.salary,
            "status": data.status,
            "user_public_id": user_public_id_str,
            "parsed_required_skills": getattr(data, "parsed_required_skills", None),
            "parsed_required_experience": getattr(data, "parsed_required_experience", None),
            "parsed_required_education": getattr(data, "parsed_required_education", None),
            "parsed_responsibilities": getattr(data, "parsed_responsibilities", None),
            "parsed_preferred_skills": getattr(data, "parsed_preferred_skills", None),
        }
