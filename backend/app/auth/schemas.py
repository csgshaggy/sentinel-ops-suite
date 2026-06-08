from pydantic import BaseModel


# ---------------------------------------------------------
# Login Request (Frontend → Backend)
# ---------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


# ---------------------------------------------------------
# User object returned after login/session restore
# ---------------------------------------------------------
class UserSession(BaseModel):
    id: int
    username: str
    role: str


# ---------------------------------------------------------
# Login Response (Backend → Frontend)
# ---------------------------------------------------------
class LoginResponse(BaseModel):
    success: bool
    user: UserSession | None = None
