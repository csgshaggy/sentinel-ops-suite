# /app/utils/sessions.py
# SentinelOps — Session Utilities (Complete + Correct)

from datetime import datetime, timedelta
from fastapi import Request
from sqlalchemy.orm import Session as DBSession

from app.models.session import Session as SessionModel
from app.models.user import User


COOKIE_NAME = "session_id"
SESSION_LIFETIME_HOURS = 1


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def _get_cookie(request: Request) -> str | None:
    return request.cookies.get(COOKIE_NAME)


def get_session_by_id(db: DBSession, token: str) -> SessionModel | None:
    """
    Public wrapper around the session fetch logic.
    """
    return (
        db.query(SessionModel)
        .filter(SessionModel.id == token)
        .first()
    )


def is_session_valid(sess: SessionModel) -> bool:
    """
    Public wrapper around the session validity logic.
    """
    now = datetime.utcnow()

    # Hard expiration
    if sess.expires_at < now:
        return False

    # Optional is_active flag
    is_active_attr = getattr(sess, "is_active", None)
    if is_active_attr is None:
        return True

    return bool(is_active_attr)


# ---------------------------------------------------------
# Session Creation
# ---------------------------------------------------------

def create_session(db: DBSession, user_id: int) -> SessionModel:
    """
    Creates a new session row for the user.
    Only uses fields that actually exist in the Session model.
    """
    now = datetime.utcnow()
    expires = now + timedelta(hours=SESSION_LIFETIME_HOURS)

    # Only include fields that exist in your Session model
    sess = SessionModel(
        user_id=user_id,
        expires_at=expires,
        created_at=now,   # safe: your model includes this
        # ❌ removed: is_active=True (your model does not have this)
    )

    db.add(sess)
    db.commit()
    db.refresh(sess)

    return sess


# ---------------------------------------------------------
# Request-Based Validators (used by /me, restore, heartbeat)
# ---------------------------------------------------------

def validate_session(request: Request, db: DBSession) -> User | None:
    """
    Lightweight validation used by /api/users/me.
    """
    token = _get_cookie(request)
    if not token:
        return None

    sess = get_session_by_id(db, token)
    if not sess:
        return None

    if not is_session_valid(sess):
        return None

    return sess.user


def restore_session(request: Request, db: DBSession):
    """
    Used by /api/auth/session/restore.
    """
    token = _get_cookie(request)
    if not token:
        return None

    sess = get_session_by_id(db, token)
    if not sess:
        return None

    if not is_session_valid(sess):
        return None

    return {
        "session_token": sess.id,
        "user": {
            "id": sess.user.id,
            "username": sess.user.username,
        },
    }


def heartbeat(request: Request, db: DBSession) -> bool:
    """
    Used by /api/auth/heartbeat.
    """
    token = _get_cookie(request)
    if not token:
        return False

    sess = get_session_by_id(db, token)
    if not sess:
        return False

    if not is_session_valid(sess):
        return False

    return True
