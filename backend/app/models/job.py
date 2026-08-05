import uuid
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime, UTC

from sqlalchemy import (
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

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    title = Column(String(255), nullable=False)

    company = Column(String(255), nullable=False)

    location = Column(String(255), nullable=True)

    description = Column(Text, nullable=True)

    required_skills = Column(JSON, nullable=True)

    experience = Column(String(100), nullable=True)

    education = Column(String(100), nullable=True)

    # Parsed job description data
    parsed_required_skills = Column(JSON, nullable=True)

    parsed_required_experience = Column(String(255), nullable=True)

    parsed_required_education = Column(String(255), nullable=True)

    parsed_responsibilities = Column(JSON, nullable=True)

    parsed_preferred_skills = Column(JSON, nullable=True)

    employment_type = Column(
        Enum(EmploymentType),
        nullable=True,
    )

    salary = Column(String(100), nullable=True)

    status = Column(
        Enum(JobStatus),
        default=JobStatus.DRAFT,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.now(UTC),
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    user = relationship(
        "User",
        back_populates="jobs",
    )

    job_matches = relationship(
        "JobMatch",
        back_populates="job",
        cascade="all, delete-orphan",
    )
