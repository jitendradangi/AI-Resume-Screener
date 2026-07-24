from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict

from app.models.enums import ProcessingStatus
from app.schemas.common import BaseSchema

class ResumeBase(BaseSchema):
    """Common resume fields."""

    filename: str
    original_filename: str
    filetype: str
    filesize: int


class ResumeUploadResponse(BaseSchema):
    """Response after uploading a resume."""

    public_id: UUID
    message: str


class ResumeResponse(BaseSchema):
    """Resume details returned to clients."""

    id: int
    public_id: UUID
    filename: str
    original_filename: str
    filetype: str
    filesize: int

    processing_status: ProcessingStatus
    processing_error: str | None = None

    uploaded_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)