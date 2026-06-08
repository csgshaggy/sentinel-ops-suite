# backend/app/schemas/api_keys.py
# SentinelOps — API Key Schemas

from datetime import datetime
from pydantic import BaseModel


class ApiKeyRead(BaseModel):
    id: int
    name: str
    created_at: datetime | None = None
    last_used: datetime | None = None


class ApiKeyCreate(BaseModel):
    name: str


class ApiKeyCreateResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    plaintext_key: str
