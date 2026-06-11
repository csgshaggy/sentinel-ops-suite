from pydantic import BaseModel, Field

class AdminUpdatePreferences(BaseModel):
    theme: str = Field(..., regex="^(system|light|dark|neon)$")
    accent: str
    timezone: str
    language: str
    login_alerts: int
    security_warnings: int
    product_updates: int
    session_timeout: int = Field(..., ge=5, le=120)
