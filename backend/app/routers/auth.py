# backend/app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.core import security
from app import models

router = APIRouter(prefix="/auth", tags=["auth"])


# ---------------------------------------------------------------------------
# REQUEST MODELS
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    username: str
    password: str


# ---------------------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------------------

@router.post("/login")
async def login(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Authenticate a user, verify password, and establish a session.
    """

    username = payload.username
    password = payload.password

    # Fetch user
    user = (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )

    # Invalid credentials
    if not user or not security.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Store session data
    request.session["user_id"] = user.id
    request.session["username"] = user.username

    return {
        "status": "ok",
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
        },
    }


# ---------------------------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------------------------

@router.post("/logout")
async def logout(request: Request):
    """
    Clear the session and log the user out.
    """
    request.session.clear()
    return {"status": "ok", "message": "Logged out"}
