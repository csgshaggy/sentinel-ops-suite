# /home/ubuntu/sentinel-ops-suite/backend/app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    # ---------------------------------------------------------
    # DATABASE CONFIG (MySQL)
    # ---------------------------------------------------------
    DB_HOST: str = Field(...)
    DB_PORT: int = Field(...)
    DB_USER: str = Field(...)
    DB_PASSWORD: str = Field(...)
    DB_NAME: str = Field(...)

    # Computed database URL (optional convenience)
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # ---------------------------------------------------------
    # JWT CONFIG
    # ---------------------------------------------------------
    JWT_SECRET: str = Field(...)
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    # ---------------------------------------------------------
    # SESSION CONFIG
    # ---------------------------------------------------------
    SESSION_SECRET: str = Field(...)
    SESSION_COOKIE_NAME: str = Field(default="sentinel_session")
    SESSION_COOKIE_SECURE: bool = Field(default=True)
    SESSION_COOKIE_HTTPONLY: bool = Field(default=True)
    SESSION_COOKIE_SAMESITE: str = Field(default="lax")

    # REQUIRED — fixes your current crash
    SESSION_EXPIRE_HOURS: int = Field(default=12)

    # ---------------------------------------------------------
    # ENVIRONMENT + CORS
    # ---------------------------------------------------------
    ENVIRONMENT: str = Field(default="production")
    CORS_ALLOWED_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])

    # ---------------------------------------------------------
    # LOGGING + PLUGINS
    # ---------------------------------------------------------
    LOG_LEVEL: str = Field(default="info")
    ENABLE_AUDIT_LOGS: bool = Field(default=True)
    ENABLE_PLUGIN_SYSTEM: bool = Field(default=True)

    # ---------------------------------------------------------
    # Pydantic Settings Config
    # ---------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # prevents crashes from unexpected env vars
    )


settings = Settings()
