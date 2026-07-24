from pydantic import ConfigDict, EmailStr, Field

from app.models.enums import UserRole
from app.schemas.common import BaseResponseSchema, BaseSchema


class UserBase(BaseSchema):
    """Common user fields."""

    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseSchema):
    """Schema for user login."""

    email: EmailStr
    password: str


class Token(BaseSchema):
    """JWT token response schema."""

    access_token: str
    token_type: str = "bearer"


class UserUpdate(BaseSchema):
    """Schema for updating user details."""

    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserResponse(BaseResponseSchema):
    """Schema returned to clients."""

    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True)