import uuid
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.enums import ProcessingStatus


class Resume(Base):
    __tablename__ = "resumes"

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

    filename = Column(String(255), nullable=False)

    original_filename = Column(String(255), nullable=False)

    filepath = Column(String(500), nullable=False)

    filetype = Column(String(100), nullable=False)

    filesize = Column(Integer, nullable=False)

    processing_status = Column(
        Enum(ProcessingStatus),
        default=ProcessingStatus.PENDING,
        nullable=False,
    )

    processing_error = Column(Text, nullable=True)

    uploaded_at = Column(
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
        back_populates="resumes",
    )

    analysis = relationship(
        "ResumeAnalysis",
        back_populates="resume",
        uselist=False,
        cascade="all, delete-orphan",
    )

    ats_reports = relationship(
        "ATSReport",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    job_matches = relationship(
        "JobMatch",
        back_populates="resume",
        cascade="all, delete-orphan",
    )
