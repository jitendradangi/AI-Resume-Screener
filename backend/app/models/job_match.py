import uuid
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime, UTC

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database.base import Base
from sqlalchemy import UniqueConstraint

class JobMatch(Base):
    __tablename__ = "job_matches"

    __table_args__ = (
        UniqueConstraint(
            "resume_id",
            "job_id",
            name="uq_resume_job_match",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    public_id = Column(
       CHAR(36),
       default=lambda: str(uuid.uuid4()),
       unique=True,
       nullable=False,
       index=True,
    )

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
    )

    match_score = Column(Integer, nullable=False)

    matched_skills = Column(JSON, nullable=True)

    missing_skills = Column(JSON, nullable=True)

    # Detailed skill matching analysis
    matched_preferred_skills = Column(JSON, nullable=True)

    extra_skills = Column(JSON, nullable=True)

    skill_match_breakdown = Column(JSON, nullable=True)

    # Experience matching analysis
    candidate_years = Column(Integer, nullable=True)

    required_min_years = Column(Integer, nullable=True)

    required_max_years = Column(Integer, nullable=True)

    experience_match_score = Column(Integer, nullable=True)

    experience_match_breakdown = Column(JSON, nullable=True)

    # Education matching analysis
    candidate_degree = Column(String(100), nullable=True)

    candidate_level = Column(Integer, nullable=True)

    required_degree = Column(String(100), nullable=True)

    required_level = Column(Integer, nullable=True)

    education_match_score = Column(Integer, nullable=True)

    education_match_breakdown = Column(JSON, nullable=True)

    # Project matching analysis
    has_projects = Column(Boolean, nullable=True)

    relevant_projects_count = Column(Integer, nullable=True)

    total_projects_count = Column(Integer, nullable=True)

    project_match_score = Column(Integer, nullable=True)

    project_match_breakdown = Column(JSON, nullable=True)

    # Semantic matching analysis (AI-powered)
    semantic_score = Column(Integer, nullable=True)

    semantic_strengths = Column(JSON, nullable=True)

    semantic_weaknesses = Column(JSON, nullable=True)

    semantic_reason = Column(Text, nullable=True)

    # Overall match analysis
    overall_match = Column(Integer, nullable=True)

    match_level = Column(String(50), nullable=True)

    # Component scores for detailed breakdown
    skill_match_score = Column(Integer, nullable=True)

    experience_match_score = Column(Integer, nullable=True)

    education_match_score = Column(Integer, nullable=True)

    project_match_score = Column(Integer, nullable=True)

    semantic_match_score = Column(Integer, nullable=True)

    ats_score = Column(Integer, nullable=True)

    recommendation = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    resume = relationship(
        "Resume",
        back_populates="job_matches",
    )

    job = relationship(
        "Job",
        back_populates="job_matches",
    )