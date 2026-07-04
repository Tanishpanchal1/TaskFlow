"""Comment endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.core.constants import UserRole
from app.crud.comment import comment
from app.crud.task import task as task_crud
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentOut

router = APIRouter()


@router.post("/tasks/{task_id}/comments", response_model=CommentOut)
async def add_comment(task_id: int, payload: CommentCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_task = await task_crud.get(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    data = payload.model_dump(exclude={"task_id"})
    data["task_id"] = task_id
    data["author_id"] = current_user.id
    return await comment.create(db, data)


@router.get("/tasks/{task_id}/comments", response_model=list[CommentOut])
async def list_comments(task_id: int, db: AsyncSession = Depends(get_db)):
    return await comment.get_comments_by_task(db, task_id)


@router.delete("/comments/{comment_id}", response_model=CommentOut)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_comment = await comment.get(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if current_user.role != UserRole.ADMIN.value and db_comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    deleted = await comment.remove(db, comment_id)
    return deleted
