from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# Generic type for reusable response models
T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with ORM support."""

    model_config = ConfigDict(from_attributes=True)


class PublicIDSchema(BaseSchema):
    """Schema containing public UUID."""

    public_id: UUID


class TimestampSchema(BaseSchema):
    """Schema containing timestamps."""

    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseSchema):
    """Simple success/error response."""

    success: bool = True
    message: str


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""

    success: bool = True
    message: str = "Data fetched successfully"

    total: int
    page: int
    page_size: int
    total_pages: int

    data: List[T]


class ErrorResponse(BaseSchema):
    """Standard error response."""

    success: bool = False
    message: str
    errors: Optional[list[str]] = None

class BaseResponseSchema(
    PublicIDSchema,
    TimestampSchema,
):
    """Common fields for all response schemas."""
    pass