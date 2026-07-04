"""User endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db, require_role
from app.core.constants import UserRole
from app.crud.user import user
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserOut, summary="Current user", description="Return the authenticated user profile.")
async def read_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/{user_id}", response_model=UserOut, summary="Get user by id", description="Admin-only access to any user.")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_role(UserRole.ADMIN))):
    db_user = await user.get(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.patch("/me", response_model=UserOut, summary="Update profile", description="Update the authenticated user's profile.")
async def update_me(payload: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    data = payload.model_dump(exclude_unset=True, exclude={"password"})
    if payload.password:
        from app.core.security import hash_password

        data["hashed_password"] = hash_password(payload.password)
    return await user.update(db, current_user, data)
