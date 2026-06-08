# /home/ubuntu/sentinel-ops-suite/backend/app/schemas/user.py
# SentinelOps — Unified User Schemas (Pydantic v2)

from pydantic import BaseModel, ConfigDict
from typing import Optional


# ---------------------------------------------------------
# Base user representation (shared fields)
# ---------------------------------------------------------
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None        # <-- CHANGED
    role: str
    mfa_enabled: bool

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# User returned to frontend (/api/users/me, login, AuthContext)
# ---------------------------------------------------------
class UserOut(UserBase):
    id: int
    avatar_url: Optional[str] = None
    avatar_thumb_url: Optional[str] = None


# ---------------------------------------------------------
# Admin: create user
# ---------------------------------------------------------
class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None        # <-- CHANGED
    password: str
    role: str = "user"


# ---------------------------------------------------------
# Admin: update user
# ---------------------------------------------------------
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None        # <-- CHANGED
    password: Optional[str] = None
    role: Optional[str] = None
    mfa_enabled: Optional[bool] = None
