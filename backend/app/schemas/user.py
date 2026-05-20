# /home/ubuntu/sentinel-ops-suite/backend/app/schemas/user.py
# SentinelOps — User Schemas (Pydantic v2, Session-Based Auth)

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------
# Base user representation
# ---------------------------------------------------------
class UserBase(BaseModel):
    email: str
    role: str
    is_active: bool


# ---------------------------------------------------------
# User returned to frontend
# ---------------------------------------------------------
class UserRead(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
