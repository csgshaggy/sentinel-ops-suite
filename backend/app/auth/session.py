# /app/auth/session.py
# SentinelOps — Session Management Subsystem

import uuid
from datetime import datetime, timedelta

from fastapi import Request
from sqlalchemy.orm import Session as DBSession

from app.models.session import Session as SessionModel
from app.models.user import User


SESSION_TTL_SECONDS = 3600  # 1 hour


# ---------------------------------------------------------
# Create a new session for a user
# ---------------------------------------------------------
def create_session(db: DBSession, user_id: int) -> SessionModel:
    """
    Creates a new session row for the given user.
    """
    session_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(seconds=SESSION_TTL_SECONDS)

    new_session = SessionModel(
        id=session_id,
        user_id=user_id,
        expires_at=expires_at,
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session


# ---------------------------------------------------------
# Invalidate a single session (delete)
# ---------------------------------------------------------
def invalidate_session(db: DBSession, session_id: str) -> None:
    """
    Deletes a session by ID.
    """
    db.query(SessionModel).filter(SessionModel.id == session_id).delete()
    db.commit()


# ---------------------------------------------------------
# Invalidate all sessions for a user (single-session policy)
# ---------------------------------------------------------
def invalidate_all_sessions_for_user(db: DBSession, user_id: int) -> None:
    """
    Deletes all sessions for a given user.
    """
    db.query(SessionModel).filter(SessionModel.user_id == user_id).delete()
    db.commit()


# ---------------------------------------------------------
# Retrieve an active session (no renewal)
# ---------------------------------------------------------
def get_active_session(db: DBSession, session_id: str) -> SessionModel | None:
    """
    Returns the session if it exists and is not expired.
    Deletes expired sessions automatically.
    """
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if not session:
        return None

    # Expired → delete it
    if session.expires_at < datetime.utcnow():
        db.delete(session)
        db.commit()
        return None

    return session


# ---------------------------------------------------------
# Resolve user from session cookie
# ---------------------------------------------------------
def get_session_user(request: Request, db: DBSession) -> User | None:
    """
    Retrieves the authenticated user based on the session cookie.
    Returns None if no valid session exists.
    """

    session_id = request.cookies.get("session_id")
    if not session_id:
        return None

    session = get_active_session(db, session_id)
    if not session:
        return None

    user = db.query(User).filter(User.id == session.user_id).first()
    return user

