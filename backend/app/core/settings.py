# /home/ubuntu/sentinel-ops-suite/backend/app/core/settings.py

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    # ---------------------------------------------------------
    # DATABASE CONFIG (MySQL)
    # ---------------------------------------------------------
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # ---------------------------------------------------------
    # JWT CONFIG (kept for compatibility)
    # ---------------------------------------------------------
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ---------------------------------------------------------
    # SESSION CONFIG (REQUIRED FOR SessionMiddleware)
    # ---------------------------------------------------------
    SESSION_SECRET: str                     # your existing session secret
    SESSION_COOKIE_NAME: str = "sentinel_session"
    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "none"   # ⭐ must be "none" for cross-path cookies
    SESSION_EXPIRE_HOURS: int = 12          # ⭐ required field

    # ---------------------------------------------------------
    # SECRET KEY FOR SIGNING SESSION COOKIES
    # (SessionMiddleware requires this)
    # ---------------------------------------------------------
    SECRET_KEY: str = "CHANGE_ME_TO_A_SECURE_RANDOM_STRING"

    # ---------------------------------------------------------
    # ENVIRONMENT + CORS
    # ---------------------------------------------------------
    ENVIRONMENT: str = "production"
    CORS_ALLOWED_ORIGINS: List[str] = Field(default_factory=list)

    # ---------------------------------------------------------
    # LOGGING + PLUGINS
    # ---------------------------------------------------------
    LOG_LEVEL: str = "info"
    ENABLE_AUDIT_LOGS: bool = True
    ENABLE_PLUGIN_SYSTEM: bool = True

    # ---------------------------------------------------------
    # Pydantic Settings Config
    # ---------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
