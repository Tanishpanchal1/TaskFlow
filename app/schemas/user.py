"""User schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.constants import UserRole


class UserSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str | None = None
    role: str


class UserBase(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None


class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None


class UserUpdate(UserBase):
    is_active: bool | None = None
    role: UserRole | None = None
    password: str | None = Field(default=None, min_length=8)


class UserOut(UserSummary):
    created_at: datetime
    is_active: bool


class UserMeOut(UserOut):
    pass