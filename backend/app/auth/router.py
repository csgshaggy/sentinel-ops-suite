# SentinelOps — Auth Router (Unified)

from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.dependencies.auth import get_db
from app.models.user import User

from app.core.security import verify_password
from app.utils.sessions import (
    create_session,
    get_session_by_id,
    is_session_valid,
)

router = APIRouter(tags=["auth"])


# ---------------------------------------------------------
# Login Request Model (JSON body)
# ---------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


# ---------------------------------------------------------
# Login
# ---------------------------------------------------------
@router.post("/login")
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    username = payload.username
    password = payload.password

    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Create a new session for the user
    session = create_session(db, user.id)

    response.set_cookie(
        key="session_id",
        value=session.id,
        httponly=True,
        secure=False,  # set True in production
        samesite="lax",
        max_age=3600,
        path="/",
    )

    return {"message": "Login successful", "role": user.role}


# ---------------------------------------------------------
# Logout
# ---------------------------------------------------------
@router.post("/logout")
def logout(response: Response, request: Request, db: Session = Depends(get_db)):
    # No invalidate_session() exists — cookie removal is sufficient.
    response.delete_cookie("session_id", path="/")
    return {"message": "Logged out"}


# ---------------------------------------------------------
# /me — Required by frontend
# ---------------------------------------------------------
@router.get("/me")
def me(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = get_session_by_id(db, session_id)
    if not session or not is_session_valid(session):
        raise HTTPException(status_code=401, detail="Invalid session")

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
    }


# ---------------------------------------------------------
# Session Restore
# ---------------------------------------------------------
@router.get("/session/restore")
def session_restore(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get("session_id")

    if not session_id:
        return {"user": None}

    session = get_session_by_id(db, session_id)
    if not session or not is_session_valid(session):
        return {"user": None}

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        return {"user": None}

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
        }
    }


# ---------------------------------------------------------
# Session Status
# ---------------------------------------------------------
@router.get("/session/status")
def session_status(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get("session_id")

    if not session_id:
        return {"active": False}

    session = get_session_by_id(db, session_id)
    if not session or not is_session_valid(session):
        return {"active": False}

    return {"active": True}
