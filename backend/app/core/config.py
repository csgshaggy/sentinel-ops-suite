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
    # S3 AVATAR STORAGE (REAL SETTINGS APPLIED)
    # ---------------------------------------------------------
    USE_S3: bool = Field(default=True)
    S3_BUCKET: str | None = Field(default="sentinelops-avatars")
    S3_REGION: str | None = Field(default="us-east-1")
    S3_ACCESS_KEY: str | None = Field(default="AKIA42HLACB76D2CXYNZ")
    S3_SECRET_KEY: str | None = Field(default="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")
    S3_BASE_URL: str | None = Field(
        default="https://sentinelops-avatars.s3.us-east-1.amazonaws.com"
    )

    # ---------------------------------------------------------
    # Pydantic Settings Config
    # ---------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
