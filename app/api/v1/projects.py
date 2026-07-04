"""Project endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.core.constants import UserRole
from app.crud.project import project
from app.crud.team import team
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.utils.permissions import is_admin

router = APIRouter()


@router.post("", response_model=ProjectOut)
async def create_project(payload: ProjectCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_team = await team.get(db, payload.team_id)
    if db_team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    if not is_admin(current_user) and not await team.is_member(db, db_team.id, current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return await project.create(db, payload)


@router.get("", response_model=list[ProjectOut])
async def list_projects(db: AsyncSession = Depends(get_db)):
    return await project.get_multi(db)


@router.get("/{project_id}", response_model=ProjectOut)
async def read_project(project_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_project = await project.get(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    db_team = await team.get(db, db_project.team_id)
    if db_team is None or (not is_admin(current_user) and not await team.is_member(db, db_team.id, current_user.id)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return db_project


@router.patch("/{project_id}", response_model=ProjectOut)
async def update_project(project_id: int, payload: ProjectUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_project = await project.get(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    db_team = await team.get(db, db_project.team_id)
    if db_team is None or (not is_admin(current_user) and not await team.is_member(db, db_team.id, current_user.id)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return await project.update(db, db_project, payload)


@router.delete("/{project_id}", response_model=ProjectOut)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_project = await project.get(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    db_team = await team.get(db, db_project.team_id)
    if db_team is None or (not is_admin(current_user) and not await team.is_member(db, db_team.id, current_user.id)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    deleted = await project.remove(db, project_id)
    return deleted
