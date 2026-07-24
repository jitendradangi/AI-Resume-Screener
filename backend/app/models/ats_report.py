import uuid
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class ATSReport(Base):
    __tablename__ = "ats_reports"

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

    # Overall ATS Score
    overall_score = Column(Integer, nullable=False)

    # Score Breakdown
    skills_score = Column(Integer, nullable=True)
    keyword_score = Column(Integer, nullable=True)
    experience_score = Column(Integer, nullable=True)
    education_score = Column(Integer, nullable=True)
    formatting_score = Column(Integer, nullable=True)
    grammar_score = Column(Integer, nullable=True)

    # AI Feedback
    strengths = Column(JSON, nullable=True)
    weaknesses = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    missing_keywords = Column(JSON, nullable=True)

    # AI Metadata
    ai_model = Column(String(100), nullable=True)
    analysis_version = Column(String(20), nullable=True)
    processing_time_ms = Column(Integer, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    resume = relationship(
        "Resume",
        back_populates="ats_reports",
    )