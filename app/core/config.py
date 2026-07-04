"""
Centralized application configuration.

All environment variables are loaded from .env
using Pydantic Settings.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --------------------------------------------------------
    # Application
    # --------------------------------------------------------

    PROJECT_NAME: str = "TaskFlow"

    PROJECT_DESCRIPTION: str = (
        "Production Ready Task Management Backend"
    )

    VERSION: str = "0.1.0"

    ENVIRONMENT: str = "development"

    DEBUG: bool = True

    API_V1_PREFIX: str = "/api/v1"

    # --------------------------------------------------------
    # Security
    # --------------------------------------------------------

    SECRET_KEY: str = Field(...)

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------

    DATABASE_URL: str

    # --------------------------------------------------------
    # Redis
    # --------------------------------------------------------

    REDIS_URL: str

    # --------------------------------------------------------
    # CORS
    # --------------------------------------------------------

    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached settings object.

    The .env file is read only once during the
    application's lifetime.
    """
    return Settings()


settings = get_settings()