"""Shared FastAPI dependencies."""

from collections.abc import Callable

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import UserRole
from app.core.security import TOKEN_TYPE_ACCESS, decode_token
from app.crud.user import user
from app.db.session import get_db
from app.models.user import User
from app.utils.permissions import is_admin


async def get_current_user(
    authorization: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload = decode_token(token, expected_type=TOKEN_TYPE_ACCESS)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    db_user = await user.get_by_email(db, payload["sub"])
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return db_user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user


def require_role(role: UserRole) -> Callable:
    async def dependency(current_user: User = Depends(get_current_active_user)) -> User:
        current_role = getattr(current_user.role, "value", current_user.role)
        if current_role != role.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return dependency
