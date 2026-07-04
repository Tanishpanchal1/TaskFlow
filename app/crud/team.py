"""Team CRUD operations."""

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.team import Team, team_members
from app.models.user import User
from app.schemas.team import TeamCreate, TeamUpdate


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    async def add_member(self, db: AsyncSession, team: Team, user: User) -> Team:
        await db.execute(insert(team_members).values(user_id=user.id, team_id=team.id))
        await db.commit()
        refreshed = await self.get(db, team.id)
        return refreshed or team

    async def remove_member(self, db: AsyncSession, team: Team, user: User) -> Team:
        await db.execute(
            delete(team_members).where(
                team_members.c.user_id == user.id,
                team_members.c.team_id == team.id,
            )
        )
        await db.commit()
        refreshed = await self.get(db, team.id)
        return refreshed or team

    async def is_member(self, db: AsyncSession, team_id: int, user_id: int) -> bool:
        result = await db.execute(
            select(team_members.c.user_id).where(
                team_members.c.team_id == team_id,
                team_members.c.user_id == user_id,
            )
        )
        return result.first() is not None

    async def get_teams_for_user(self, db: AsyncSession, user_id: int) -> list[Team]:
        result = await db.execute(select(Team).join(Team.members).where(User.id == user_id))
        return list(result.scalars().unique().all())


team = CRUDTeam(Team)