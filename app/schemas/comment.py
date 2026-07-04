"""Comment schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentBase(BaseModel):
    content: str = Field(min_length=1, max_length=10_000)


class CommentCreate(CommentBase):
    task_id: int | None = None


class CommentUpdate(BaseModel):
    content: str | None = Field(default=None, min_length=1, max_length=10_000)


class CommentOut(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    author_id: int
    created_at: datetime