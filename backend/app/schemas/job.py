from datetime import datetime

from pydantic import ConfigDict, Field

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