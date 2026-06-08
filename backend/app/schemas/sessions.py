# backend/app/schemas/sessions.py

from datetime import datetime
from pydantic import BaseModel


class SessionRead(BaseModel):
  id: str
  ip: str | None = None
  user_agent: str | None = None
  location: str | None = None
  last_active: datetime | None = None


class SessionTerminateResponse(BaseModel):
  success: bool
  message: str
