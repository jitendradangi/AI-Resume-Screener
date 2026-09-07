import uuid
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    Text,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"


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
        unique=True,
    )

    # Complete extracted resume text
    raw_text = Column(Text, nullable=False)

    # Complete parsed resume
    parsed_data = Column(JSON, nullable=True)

    # Frequently used fields
    summary = Column(Text, nullable=True)

    skills = Column(JSON, nullable=True)

    education = Column(JSON, nullable=True)

    experience = Column(JSON, nullable=True)

    projects = Column(JSON, nullable=True)

    certifications = Column(JSON, nullable=True)

    languages = Column(JSON, nullable=True)

    # Gemini AI analysis result (Step 6)
    ai_analysis = Column(JSON, nullable=True)

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

    resume = relationship(
        "Resume",
        back_populates="analysis",
    )