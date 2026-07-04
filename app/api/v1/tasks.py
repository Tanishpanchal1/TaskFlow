"""Task endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.core.constants import TaskPriority, TaskStatus
from app.core.constants import UserRole
from app.crud.project import project
from app.crud.task import task
from app.crud.team import team
from app.models.user import User
from app.schemas.task import TaskAssignUpdate, TaskCreate, TaskOut, TaskStatusUpdate, TaskUpdate
from app.utils.permissions import is_admin

router = APIRouter()


@router.post("", response_model=TaskOut)
async def create_task(payload: TaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_project = await project.get(db, payload.project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    db_team = await team.get(db, db_project.team_id)
    if db_team is None or (not is_admin(current_user) and not await team.is_member(db, db_team.id, current_user.id)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return await task.create(db, payload)


@router.get("", response_model=list[TaskOut])
async def list_tasks(
    project_id: int = Query(...),
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    priority: TaskPriority | None = None,
    assigned_to_id: int | None = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    return await task.get_tasks_by_project(db, project_id, status_filter, assigned_to_id, priority, limit, offset)


@router.get("/{task_id}", response_model=TaskOut)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    db_task = await task.get(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task


@router.patch("/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, payload: TaskUpdate, db: AsyncSession = Depends(get_db)):
    db_task = await task.get(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return await task.update(db, db_task, payload)


@router.delete("/{task_id}", response_model=TaskOut)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await task.remove(db, task_id)
    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return deleted


@router.patch("/{task_id}/assign", response_model=TaskOut)
async def assign_task(task_id: int, payload: TaskAssignUpdate, db: AsyncSession = Depends(get_db)):
    db_task = await task.get(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return await task.assign_task(db, db_task, payload.assigned_to_id)


@router.patch("/{task_id}/status", response_model=TaskOut)
async def change_task_status(task_id: int, payload: TaskStatusUpdate, db: AsyncSession = Depends(get_db)):
    db_task = await task.get(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db_task.status = payload.status
    await db.commit()
    await db.refresh(db_task)
    return db_task
