# /home/ubuntu/sentinel-ops-suite/backend/app/schemas/audit.py
# SentinelOps — Audit Log Schemas (Pydantic v2)

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AuditLogRead(BaseModel):
    id: int
    timestamp: datetime
    actor_email: str | None
    action: str
    target: str | None
    details: str | None

    model_config = ConfigDict(from_attributes=True)
