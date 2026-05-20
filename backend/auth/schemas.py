from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str
    is_active: bool


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "viewer"


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
