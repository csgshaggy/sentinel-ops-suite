# /app/auth/session.py
# SentinelOps — Session Management Subsystem

import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from auth.models import Session as SessionModel


# ---------------------------------------------------------
# Create a new session for a user
# ---------------------------------------------------------
def create_session(
    db: Session,
    user_id: int,
    duration_minutes: int = 60,
) -> SessionModel:
    session_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=duration_minutes)

    new_session = SessionModel(
        id=session_id,
        user_id=user_id,
        is_active=True,
        expires_at=expires_at,
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session


# ---------------------------------------------------------
# Invalidate a single session
# ---------------------------------------------------------
def invalidate_session(db: Session, session_id: str) -> None:
    session = (
        db.query(SessionModel)
        .filter(SessionModel.id == session_id)
        .first()
    )

    if session:
        session.is_active = False
        db.commit()


# ---------------------------------------------------------
# Invalidate all sessions for a user
# (Used for single-active-session enforcement)
# ---------------------------------------------------------
def invalidate_all_sessions_for_user(db: Session, user_id: int) -> None:
    db.query(SessionModel).filter(
        SessionModel.user_id == user_id,
        SessionModel.is_active == True,
    ).update({"is_active": False})

    db.commit()


# ---------------------------------------------------------
# Retrieve an active session (no renewal)
# ---------------------------------------------------------
def get_active_session(db: Session, session_id: str) -> SessionModel | None:
    session = (
        db.query(SessionModel)
        .filter(
            SessionModel.id == session_id,
            SessionModel.is_active == True,
        )
        .first()
    )

    if not session:
        return None

    # Expiration check
    if session.expires_at < datetime.utcnow():
        session.is_active = False
        db.commit()
        return None

    return session
