from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    role: str
    is_active: bool


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "viewer"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
