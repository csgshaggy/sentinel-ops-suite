# backend/app/routers/sessions.py
# SentinelOps — Unified Session Management Router (Upgraded)
# NOTE:
#   This router intentionally uses prefix="/sessions"
#   and is mounted in main.py with:
#       app.include_router(sessions_router, prefix="/api/auth", tags=["sessions"])
#   Final routes become:
#       /api/auth/sessions
#       /api/auth/sessions/terminate-others
#       /api/auth/sessions/{target_session_id}

from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import get_db
from app.core.sessions import (
    get_session_by_id,
    get_sessions_for_user,
    delete_session,
)
from app.models.session import Session as SessionModel

router = APIRouter(prefix="/sessions", tags=["sessions"])


# ------------------------------------------------------------
# Helper — authenticated user + current session
# ------------------------------------------------------------
def get_current_user_and_session(session_id: str | None, db: Session):
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = get_session_by_id(db, session_id)
    if not session or session.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired")

    return session.user_id, session


# ------------------------------------------------------------
# GET /api/auth/sessions — list all active sessions for user
# ------------------------------------------------------------
@router.get("")
async def list_sessions(
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user_id, current_session = get_current_user_and_session(session_id, db)

    sessions = get_sessions_for_user(db, user_id)

    return {
        "sessions": [
            {
                "session_id": s.session_id,
                "created_at": s.created_at.isoformat(),
                "expires_at": s.expires_at.isoformat(),
                "is_current": (s.session_id == current_session.session_id),
            }
            for s in sessions
        ]
    }


# ------------------------------------------------------------
# DELETE /api/auth/sessions/{target_session_id}
# ------------------------------------------------------------
@router.delete("/{target_session_id}")
async def terminate_single_session(
    target_session_id: str,
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user_id, current_session = get_current_user_and_session(session_id, db)

    target = get_session_by_id(db, target_session_id)
    if not target:
        raise HTTPException(status_code=404, detail="Session not found")

    if target.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if target.session_id == current_session.session_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot terminate the current active session",
        )

    delete_session(db, target.session_id)

    return {
        "success": True,
        "message": f"Session '{target_session_id}' terminated successfully.",
    }


# ------------------------------------------------------------
# POST /api/auth/sessions/terminate-others
# ------------------------------------------------------------
@router.post("/terminate-others")
async def terminate_other_sessions(
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user_id, current_session = get_current_user_and_session(session_id, db)

    sessions = get_sessions_for_user(db, user_id)

    terminated = 0
    for s in sessions:
        if s.session_id != current_session.session_id:
            delete_session(db, s.session_id)
            terminated += 1

    return {
        "success": True,
        "terminated": terminated,
        "message": f"Terminated {terminated} other session(s).",
    }
