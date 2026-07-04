"""Optional initial database bootstrap."""

from sqlalchemy import select

from app.core.constants import UserRole
from app.core.security import hash_password
from app.models.user import User


async def create_initial_admin(session) -> None:
    result = await session.execute(select(User).where(User.role == UserRole.ADMIN.value))
    if result.scalar_one_or_none() is None:
        session.add(
            User(
                email="admin@taskflow.local",
                hashed_password=hash_password("admin1234"),
                full_name="TaskFlow Admin",
                role=UserRole.ADMIN.value,
                is_active=True,
            )
        )
        await session.commit()