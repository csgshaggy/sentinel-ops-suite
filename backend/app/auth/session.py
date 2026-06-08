# /app/auth/session.py
# SentinelOps — Session Management Subsystem

import uuid
from datetime import datetime, timedelta

# IMPORTANT:
# Rename SQLAlchemy ORM session import to avoid collisions with your Session model.
from sqlalchemy.orm import Session as DBSession

# Rename SQLAlchemy model import to avoid collisions with DBSession.
from app.models.session import Session as SessionModel


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
