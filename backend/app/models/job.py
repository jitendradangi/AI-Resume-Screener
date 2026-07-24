import uuid
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime, UTC

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.enums import EmploymentType, JobStatus


class Job(Base):
    __tablename__ = "jobs"


    id = Column(Integer, primary_key=True, index=True)

    public_id = Column(
       CHAR(36),
       default=lambda: str(uuid.uuid4()),
       unique=True,
       nullable=False,
       index=True,
    )

    title = Column(String(255), nullable=False)

    company = Column(String(255), nullable=False)

    location = Column(String(255), nullable=True)

    employment_type = Column(
        Enum(EmploymentType),
        nullable=False,
        default=EmploymentType.FULL_TIME,
    )

    experience_required = Column(Integer, nullable=True)

    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(10),nullable=False, default="INR")

    description = Column(Text, nullable=False)

    required_skills = Column(JSON, nullable=True)

    preferred_skills = Column(JSON, nullable=True)

    education = Column(String(255), nullable=True)

    deadline = Column(DateTime(timezone=True), nullable=True)

    is_active = Column(Boolean, default=True)

    status = Column(
        Enum(JobStatus),
        default=JobStatus.OPEN,
        nullable=False,
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    creator = relationship(
        "User",
        back_populates="jobs",
    )

    job_matches = relationship(
        "JobMatch",
        back_populates="job",
        cascade="all, delete-orphan",
    )