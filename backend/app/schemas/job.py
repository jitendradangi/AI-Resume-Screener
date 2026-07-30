from datetime import datetime

from pydantic import ConfigDict, Field, model_validator

from app.models.enums import EmploymentType, JobStatus
from app.schemas.common import BaseResponseSchema, BaseSchema


# ----------------------------
# Nested Schemas
# ----------------------------

class SalarySchema(BaseSchema):
    min: int | None = None
    max: int | None = None
    currency: str = "INR"


# ----------------------------
# Base Schema
# ----------------------------

class JobBase(BaseSchema):
    title: str = Field(..., min_length=3, max_length=255)

    company: str = Field(..., min_length=2, max_length=255)

    location: str | None = None

    employment_type: EmploymentType = EmploymentType.FULL_TIME

    experience_required: int | None = None

    salary: SalarySchema | None = None

    description: str

    required_skills: list[str] = []

    preferred_skills: list[str] = []

    education: str | None = None

    deadline: datetime | None = None


# ----------------------------
# Create
# ----------------------------

class JobCreate(JobBase):
    pass


# ----------------------------
# Update
# ----------------------------

class JobUpdate(BaseSchema):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    employment_type: EmploymentType | None = None
    experience_required: int | None = None
    salary: SalarySchema | None = None
    description: str | None = None
    required_skills: list[str] | None = None
    preferred_skills: list[str] | None = None
    education: str | None = None
    deadline: datetime | None = None
    status: JobStatus | None = None
    is_active: bool | None = None


# ----------------------------
# Response
# ----------------------------

class JobResponse(
    BaseResponseSchema,
    JobBase,
):
    status: JobStatus
    is_active: bool
    created_by: str

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def resolve_job_fields(cls, data: any) -> any:
        if isinstance(data, dict):
            return data
        
        salary = {
            "min": getattr(data, "salary_min", None),
            "max": getattr(data, "salary_max", None),
            "currency": getattr(data, "salary_currency", "INR")
        }
        
        created_by_str = ""
        if hasattr(data, "creator") and data.creator:
            created_by_str = str(data.creator.public_id)
        elif hasattr(data, "created_by"):
            created_by_str = str(data.created_by)
            
        return {
            "public_id": data.public_id,
            "created_at": data.created_at,
            "updated_at": data.updated_at,
            "title": data.title,
            "company": data.company,
            "location": data.location,
            "employment_type": data.employment_type,
            "experience_required": data.experience_required,
            "salary": salary,
            "description": data.description,
            "required_skills": data.required_skills or [],
            "preferred_skills": data.preferred_skills or [],
            "education": data.education,
            "deadline": data.deadline,
            "status": data.status,
            "is_active": data.is_active,
            "created_by": created_by_str,
        }