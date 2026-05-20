# /app/auth/router.py
# SentinelOps — Auth Router

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_db
from auth.models import User
from auth.utils import verify_password
from auth.session import (
    create_session,
    invalidate_all_sessions_for_user,
    invalidate_session,
)

router = APIRouter(prefix="/auth", tags=["auth"])


# ---------------------------------------------------------
# Login
# ---------------------------------------------------------
@router.post("/login")
def login(username: str, password: str, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Enforce single active session
    invalidate_all_sessions_for_user(db, user.id)

    session = create_session(db, user.id)

    response.set_cookie(
        key="session_id",
        value=session.id,
        httponly=True,
        secure=False,  # set True in production
        samesite="lax",
        max_age=3600,
    )

    return {"message": "Login successful", "role": user.role}


# ---------------------------------------------------------
# Logout
# ---------------------------------------------------------
@router.post("/logout")
def logout(response: Response, session_id: str, db: Session = Depends(get_db)):
    invalidate_session(db, session_id)

    response.delete_cookie("session_id")

    return {"message": "Logged out"}
