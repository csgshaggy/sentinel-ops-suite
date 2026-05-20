# /backend/app/api/auth.py

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.core.sessions import (
    create_session,
    destroy_existing_sessions_for_user,
    get_session_by_id,
    refresh_session_ttl,
)
from app.core.mfa import (
    generate_pending_login_token,
    store_pending_login_token,
    validate_pending_login_token,
    verify_totp_code,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.database import get_db  # adjust if your DB dependency lives elsewhere

router = APIRouter(prefix="/api/auth", tags=["auth"])

SESSION_COOKIE = "session_id"
SESSION_TTL = timedelta(minutes=15)


# ------------------------------------------------------------
# Request models
# ------------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


class VerifyTOTPRequest(BaseModel):
    pending_login_token: str
    code: str


# ------------------------------------------------------------
# POST /api/auth/login
# Username + password → MFA (optional) → session
# ------------------------------------------------------------
@router.post("/login")
async def login(
    req: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    # SQLAlchemy is sync → run in threadpool
    user = await run_in_threadpool(
        UserRepository.get_by_username, db, req.username
    )

    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    # MFA required
    if getattr(user, "mfa_enabled", False):
        pending_token = generate_pending_login_token()
        store_pending_login_token(user.id, pending_token)

        return {
            "pending_login_token": pending_token,
            "mfa_required": True,
            "delivery_hint": getattr(user, "mfa_delivery_hint", None),
        }

    # No MFA → create session immediately
    await destroy_existing_sessions_for_user(user.id)

    session = await create_session(
        user_id=user.id,
        ttl=SESSION_TTL,
    )

    response.set_cookie(
        key=SESSION_COOKIE,
        value=session.session_id,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=int(SESSION_TTL.total_seconds()),
    )

    return {
        "user": user.to_public_dict(),
        "session": session.to_public_dict(),
    }


# ------------------------------------------------------------
# POST /api/auth/verify-totp
# MFA → session
# ------------------------------------------------------------
@router.post("/verify-totp")
async def verify_totp(req: VerifyTOTPRequest, response: Response):
    user_id = validate_pending_login_token(req.pending_login_token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired login token.")

    # Tortoise ORM User.get()
    user = await User.get(user_id)
    if not user or not getattr(user, "mfa_enabled", False):
        raise HTTPException(status_code=400, detail="MFA not enabled for this user.")

    if not verify_totp_code(user.mfa_secret, req.code):
        raise HTTPException(status_code=400, detail="Invalid authentication code.")

    await destroy_existing_sessions_for_user(user.id)

    session = await create_session(
        user_id=user.id,
        ttl=SESSION_TTL,
    )

    response.set_cookie(
        key=SESSION_COOKIE,
        value=session.session_id,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=int(SESSION_TTL.total_seconds()),
    )

    return {
        "user": user.to_public_dict(),
        "session": session.to_public_dict(),
    }


# ------------------------------------------------------------
# GET /api/auth/session/restore
# ------------------------------------------------------------
@router.get("/session/restore")
async def restore_session(session_id: str | None = Cookie(None)):
    if not session_id:
        return {"user": None}

    session = await get_session_by_id(session_id)
    if not session or session.is_expired():
        return {"user": None}

    user = await User.get(session.user_id)
    if not user:
        return {"user": None}

    await refresh_session_ttl(session.session_id, SESSION_TTL)

    return {
        "user": user.to_public_dict(),
        "session": session.to_public_dict(),
    }


# ------------------------------------------------------------
# GET /api/auth/heartbeat
# ------------------------------------------------------------
@router.get("/heartbeat")
async def heartbeat(session_id: str | None = Cookie(None)):
    if not session_id:
        return {"active": False}

    session = await get_session_by_id(session_id)
    if not session or session.is_expired():
        return {"active": False}

    await refresh_session_ttl(session.session_id, SESSION_TTL)
    return {"active": True}


# ------------------------------------------------------------
# POST /api/auth/logout
# Idempotent logout — never throws, even if session is expired/missing
# ------------------------------------------------------------
@router.post("/logout")
async def logout(response: Response, session_id: str | None = Cookie(None)):
    try:
        if session_id:
            # Destroy session if it exists — ignore if it doesn't
            await destroy_existing_sessions_for_user(None, session_id=session_id)
    except Exception:
        # Logout must always succeed, even if session is gone
        pass

    # Always delete cookie
    response.delete_cookie(
        key=SESSION_COOKIE,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    return {"success": True}
