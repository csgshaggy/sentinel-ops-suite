# app/schemas/session.py

from pydantic import BaseModel
from datetime import datetime


class SessionOut(BaseModel):
    session_id: str
    user_id: int
    expires_at: datetime

    class Config:
        orm_mode = True
