from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.enums import ProcessingStatus

class ResumeBase(BaseModel):
    """Common resume fields."""

    filename: str
    original_filename: str
    filetype: str
    filesize: int


class ResumeUploadResponse(BaseModel):
    """Response after uploading a resume."""

    public_id: UUID
    message: str


class ResumeResponse(BaseModel):
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

    ai_analysis: dict | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def resolve_analysis_fields(cls, data: any) -> any:
        if isinstance(data, dict):
            return data
        
        ai_analysis_data = None
        if hasattr(data, "analysis") and data.analysis:
            ai_analysis_data = getattr(data.analysis, "ai_analysis", None)
        
        return {
            "id": data.id,
            "public_id": data.public_id,
            "filename": data.filename,
            "original_filename": data.original_filename,
            "filetype": data.filetype,
            "filesize": data.filesize,
            "processing_status": data.processing_status,
            "processing_error": data.processing_error,
            "uploaded_at": data.uploaded_at,
            "updated_at": data.updated_at,
            "ai_analysis": ai_analysis_data,
        }