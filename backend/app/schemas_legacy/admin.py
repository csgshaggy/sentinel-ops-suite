# /home/ubuntu/sentinel-ops-suite/backend/app/schemas/admin.py
# SentinelOps — Admin Schemas (Pydantic v2)

from pydantic import BaseModel
from typing import List

from app.schemas.audit import AuditLogRead


class AuditLogList(BaseModel):
    logs: List[AuditLogRead]
