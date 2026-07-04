"""Team endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db, require_role
from app.core.constants import UserRole
from app.crud.team import team
from app.crud.user import user
from app.models.team import Team
from app.models.user import User
from app.schemas.team import TeamCreate, TeamOut, TeamUpdate
from app.utils.permissions import is_admin

router = APIRouter()


@router.post("", response_model=TeamOut)
async def create_team(payload: TeamCreate, db: AsyncSession = Depends(get_db), _: User = Depends(require_role(UserRole.ADMIN))):
    return await team.create(db, payload)


@router.get("", response_model=list[TeamOut])
async def list_teams(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if is_admin(current_user):
        return await team.get_multi(db)
    return await team.get_teams_for_user(db, current_user.id)


@router.get("/{team_id}", response_model=TeamOut)
async def read_team(team_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_team = await team.get(db, team_id)
    if db_team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    if not is_admin(current_user) and not await team.is_member(db, db_team.id, current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return db_team


@router.patch("/{team_id}", response_model=TeamOut)
async def update_team(team_id: int, payload: TeamUpdate, db: AsyncSession = Depends(get_db), _: User = Depends(require_role(UserRole.ADMIN))):
    db_team = await team.get(db, team_id)
    if db_team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return await team.update(db, db_team, payload)


@router.delete("/{team_id}", response_model=TeamOut)
async def delete_team(team_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_role(UserRole.ADMIN))):
    db_team = await team.remove(db, team_id)
    if db_team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return db_team


@router.post("/{team_id}/members/{user_id}", response_model=TeamOut)
async def add_member(team_id: int, user_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_role(UserRole.ADMIN))):
    db_team = await team.get(db, team_id)
    db_user = await user.get(db, user_id)
    if db_team is None or db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team or user not found")
    return await team.add_member(db, db_team, db_user)


@router.delete("/{team_id}/members/{user_id}", response_model=TeamOut)
async def remove_member(team_id: int, user_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_role(UserRole.ADMIN))):
    db_team = await team.get(db, team_id)
    db_user = await user.get(db, user_id)
    if db_team is None or db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team or user not found")
    return await team.remove_member(db, db_team, db_user)
