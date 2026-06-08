# SentinelOps — Unified Authentication Router
# DB-backed sessions + MFA-aware login + Logout
# NOTE:
#   This router intentionally has NO "/api/auth" prefix.
#   main.py must mount it like:
#       app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

from datetime import timedelta
import os

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    Cookie,
)
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password
from app.core.sessions import (
    create_session,
    get_session_by_id,
    delete_session,
)

router = APIRouter(tags=["auth"])

SESSION_COOKIE = "session_id"
SESSION_LIFETIME_SECONDS = 60 * 60 * 24  # 24 hours

# ------------------------------------------------------------
# FIXED COOKIE SETTINGS — Chrome requires SameSite=None + Secure=True
# ------------------------------------------------------------
COOKIE_SETTINGS = {
    "httponly": True,
    "secure": True,
    "samesite": "none",
    "path": "/",
    "max_age": SESSION_LIFETIME_SECONDS,
}

# ------------------------------------------------------------
# UNIFIED AVATAR DIRECTORY (matches profile.py + avatar_service.py)
# ------------------------------------------------------------
# All avatar files must live under ./static/avatars so they are served by:
#   app.mount("/static", StaticFiles(directory="static"), name="static")
# ------------------------------------------------------------

AVATAR_DIR = "static/avatars"
os.makedirs(AVATAR_DIR, exist_ok=True)


# ------------------------------------------------------------
# Request Models
# ------------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


class MFALoginCompleteRequest(BaseModel):
    user_id: int


# ------------------------------------------------------------
# POST /api/auth/login
# ------------------------------------------------------------
@router.post("/login")
async def login(
    req: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    user = await run_in_threadpool(UserRepository.get_by_username, db, req.username)

    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    # MFA required → no session yet
    if getattr(user, "mfa_enabled", False):
        return {
            "mfa_required": True,
            "user_id": user.id,
        }

    # No MFA → create session immediately
    session_id = create_session(db=db, user_id=user.id)

    payload = {
        "success": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "mfa_enabled": getattr(user, "mfa_enabled", False),
        },
    }

    # IMPORTANT: return the response object that has the cookie set
    resp = JSONResponse(payload)
    resp.set_cookie(key=SESSION_COOKIE, value=session_id, **COOKIE_SETTINGS)
    return resp


# ------------------------------------------------------------
# POST /api/auth/login/mfa-complete
# ------------------------------------------------------------
@router.post("/login/mfa-complete")
async def login_mfa_complete(
    req: MFALoginCompleteRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == req.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if not getattr(user, "mfa_enabled", False):
        raise HTTPException(status_code=400, detail="MFA is not enabled for this user.")

    session_id = create_session(db=db, user_id=user.id)

    resp = JSONResponse(
        {
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "mfa_enabled": getattr(user, "mfa_enabled", False),
            },
        }
    )

    resp.set_cookie(key=SESSION_COOKIE, value=session_id, **COOKIE_SETTINGS)
    return resp


# ------------------------------------------------------------
# POST /api/auth/logout
# ------------------------------------------------------------
@router.post("/logout")
async def logout(
    response: Response,
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    if session_id:
        delete_session(db, session_id)

    resp = JSONResponse({"success": True})
    # Ensure we delete the same cookie we set
    resp.delete_cookie(
        key=SESSION_COOKIE,
        path="/",
    )
    return resp


# ------------------------------------------------------------
# GET /api/auth/profile  (legacy-compatible)
# ------------------------------------------------------------
@router.get("/profile")
async def get_profile(
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated.")

    session = get_session_by_id(db, session_id)
    if not session or session.is_expired():
        raise HTTPException(status_code=401, detail="Session expired.")

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "mfa_enabled": getattr(user, "mfa_enabled", False),
    }


# ------------------------------------------------------------
# GET /api/auth/me  (frontend-required endpoint)
# ------------------------------------------------------------
@router.get("/me")
async def get_me(
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated.")

    session = get_session_by_id(db, session_id)
    if not session or session.is_expired():
        raise HTTPException(status_code=401, detail="Session expired.")

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "mfa_enabled": getattr(user, "mfa_enabled", False),
    }

