"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import TOKEN_TYPE_REFRESH, create_access_token, create_refresh_token, decode_token
from app.crud.user import user
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut

router = APIRouter()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/register", response_model=UserOut, summary="Register user", description="Create a new user account.")
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await user.get_by_email(db, payload.email)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return await user.create_user(db, payload)


@router.post("/login", response_model=Token, summary="Login user", description="Authenticate with email and password.")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    db_user = await user.authenticate(db, payload.email, payload.password)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    subject = db_user.email
    return Token(access_token=create_access_token(subject), refresh_token=create_refresh_token(subject))


@router.post("/refresh", response_model=Token, summary="Refresh access token", description="Issue a new access token using a valid refresh token.")
async def refresh(payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    try:
        token_payload = decode_token(payload.refresh_token, expected_type=TOKEN_TYPE_REFRESH)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    db_user = await user.get_by_email(db, token_payload["sub"])
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")
    return Token(access_token=create_access_token(db_user.email), refresh_token=create_refresh_token(db_user.email))
