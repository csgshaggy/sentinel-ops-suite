from pydantic import BaseModel, EmailStr

class AdminUserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        orm_mode = True

class AdminUserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "viewer"

class AdminUserUpdate(BaseModel):
    role: str
    is_active: bool
