"""Task CRUD operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import TaskPriority, TaskStatus
from app.crud.base import CRUDBase
from app.models.task import Task
from app.schemas.task import TaskAssignUpdate, TaskCreate, TaskUpdate


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    async def get_tasks_by_project(
        self,
        db: AsyncSession,
        project_id: int,
        status: TaskStatus | None = None,
        assigned_to_id: int | None = None,
        priority: TaskPriority | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Task]:
        stmt = select(Task).where(Task.project_id == project_id)
        if status is not None:
            stmt = stmt.where(Task.status == status)
        if assigned_to_id is not None:
            stmt = stmt.where(Task.assigned_to_id == assigned_to_id)
        if priority is not None:
            stmt = stmt.where(Task.priority == priority)
        stmt = stmt.offset(offset).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def assign_task(self, db: AsyncSession, task: Task, assigned_to_id: int | None) -> Task:
        task.assigned_to_id = assigned_to_id
        await db.commit()
        await db.refresh(task)
        return task


task = CRUDTask(Task)