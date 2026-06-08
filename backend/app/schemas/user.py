# /home/ubuntu/sentinel-ops-suite/backend/app/schemas/user.py
# SentinelOps — Unified User Schemas (Pydantic v2)

from typing import Optional
from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------
# Base user representation (shared fields)
# ---------------------------------------------------------
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    role: str
    mfa_enabled: bool

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# User returned to frontend (AuthContext, /api/users/me)
# ---------------------------------------------------------
class UserOut(UserBase):
    id: int
    avatar_url: Optional[str] = None
    avatar_thumb_url: Optional[str] = None
    avatar_version: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# Profile response (used by /api/users/me and avatar updates)
# ---------------------------------------------------------
class UserProfileResponse(UserOut):
    """
    Full user profile returned to the frontend.
    Extends UserOut with avatar fields and any future profile metadata.
    """
    pass


# ---------------------------------------------------------
# Admin: create user
# ---------------------------------------------------------
class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    password: str
    role: str = "user"

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# Admin: update user
# ---------------------------------------------------------
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    mfa_enabled: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
