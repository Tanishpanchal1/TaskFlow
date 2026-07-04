"""Comment CRUD operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    async def get_comments_by_task(self, db: AsyncSession, task_id: int) -> list[Comment]:
        result = await db.execute(select(Comment).where(Comment.task_id == task_id))
        return list(result.scalars().all())


comment = CRUDComment(Comment)