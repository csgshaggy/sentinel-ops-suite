# utils/settings.py

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Centralized application configuration using Pydantic v2 + pydantic-settings.
    All environment variables are explicitly declared to ensure strict validation
    and predictable operator-grade behavior.
    """

    # -------------------------------------------------------------------------
    # Core Application Settings
    # -------------------------------------------------------------------------
    app_name: str = Field("SSRF Command Console", description="Application name")
    debug: bool = Field(False, description="Enable debug mode")

    # -------------------------------------------------------------------------
    # Logging / Runtime Settings
    # -------------------------------------------------------------------------
    log_level: str = Field("INFO", description="Logging level")
    log_dir: str = Field("logs", description="Directory for log output")
    log_json: bool = Field(False, description="Enable JSON-formatted logs")

    # -------------------------------------------------------------------------
    # CORS Settings
    # -------------------------------------------------------------------------
    enable_cors: bool = Field(False, description="Enable CORS middleware")
    cors_origins: list[str] = Field(
        default_factory=list, description="CORS allowed origins"
    )

    # -------------------------------------------------------------------------
    # OAuth / Authentication Settings
    # -------------------------------------------------------------------------
    oauth_client_id: str = Field(..., description="OAuth client ID")
    oauth_client_secret: str = Field(..., description="OAuth client secret")
    oauth_auth_url: str = Field(..., description="OAuth authorization URL")
    oauth_token_url: str = Field(..., description="OAuth token exchange URL")
    oauth_redirect_uri: str = Field(..., description="OAuth redirect/callback URI")

    # -------------------------------------------------------------------------
    # Pydantic Settings Config
    # -------------------------------------------------------------------------
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "forbid",
    }


# Singleton instance used across the application
settings = Settings()
