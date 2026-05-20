# /backend/app/core/sessions.py

from uuid import uuid4
from datetime import datetime, timedelta

from app.db import (
    save_session,
    delete_sessions_for_user,
    get_session,
    update_session_expiry,
)


# ------------------------------------------------------------
# Destroy all sessions for a user (single-session enforcement)
# ------------------------------------------------------------
async def destroy_existing_sessions_for_user(user_id: int | None, session_id: str | None = None):
    """
    If user_id is provided → delete all sessions for that user.
    If session_id is provided → delete only that session.
    If both are None → no-op.
    """
    try:
        await delete_sessions_for_user(user_id=user_id, session_id=session_id)
    except Exception:
        # Must be idempotent — never throw
        pass


# ------------------------------------------------------------
# Create a new session
# ------------------------------------------------------------
async def create_session(user_id: int, ttl: timedelta):
    session_id = uuid4().hex
    expires_at = datetime.utcnow() + ttl

    session = await save_session(
        user_id=user_id,
        session_id=session_id,
        expires_at=expires_at,
    )

    return session


# ------------------------------------------------------------
# Retrieve a session by ID
# ------------------------------------------------------------
async def get_session_by_id(session_id: str):
    try:
        return await get_session(session_id)
    except Exception:
        return None


# ------------------------------------------------------------
# Check if a session is expired
# ------------------------------------------------------------
def is_session_expired(session) -> bool:
    if not session or not session.expires_at:
        return True
    return datetime.utcnow() >= session.expires_at


# ------------------------------------------------------------
# Refresh TTL (sliding expiration)
# ------------------------------------------------------------
async def refresh_session_ttl(session_id: str, ttl: timedelta):
    """
    Refresh the session's expiration timestamp.
    If session doesn't exist → no-op.
    """
    try:
        new_expiry = datetime.utcnow() + ttl
        await update_session_expiry(session_id, new_expiry)
    except Exception:
        # No-op — session may already be gone
        pass
