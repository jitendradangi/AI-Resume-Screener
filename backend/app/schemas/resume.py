from typing import Any
from pydantic import BaseModel
from datetime import datetime


class ResumeResponse(BaseModel):

    id: int
    filename: str
    processing_status: str
    ats_score: int | None = None
    uploaded_at: datetime
    class Config:
        from_attributes = True