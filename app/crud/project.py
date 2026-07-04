"""Project CRUD operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    async def get_projects_by_team(self, db: AsyncSession, team_id: int) -> list[Project]:
        result = await db.execute(select(Project).where(Project.team_id == team_id))
        return list(result.scalars().all())


project = CRUDProject(Project)