"""Team schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TeamBase(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    description: str | None = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = None


class TeamOut(TeamBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime