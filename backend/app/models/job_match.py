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