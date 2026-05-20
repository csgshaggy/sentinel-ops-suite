# /home/ubuntu/sentinel-ops-suite/backend/app/schemas/session.py
# SentinelOps — Session Schemas (Pydantic v2, Session-Based Auth)

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SessionRead(BaseModel):
    id: str
    user_id: int
    created_at: datetime
    expires_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
