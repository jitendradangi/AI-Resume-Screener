import uuid

from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
)
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship

from app.database.base import Base


class ATSScore(Base):
    __tablename__ = "ats_scores"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    public_id = Column(
        CHAR(36),
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
        index=True,
    )

    resume_analysis_id = Column(
        Integer,
        ForeignKey("resume_analysis.id"),
        nullable=False,
        unique=True,
    )

    overall_score = Column(Float, default=0)

    skills_score = Column(Float, default=0)

    education_score = Column(Float, default=0)

    experience_score = Column(Float, default=0)

    projects_score = Column(Float, default=0)

    format_score = Column(Float, default=0)

    section_score = Column(Float, default=0)

    keyword_score = Column(Float, default=0)

    missing_keywords = Column(JSON)

    strengths = Column(JSON)

    weaknesses = Column(JSON)

    recommendations = Column(JSON)

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

    resume_analysis = relationship(
        "ResumeAnalysis",
        back_populates="ats_score",
    )