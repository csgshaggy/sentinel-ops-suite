# app/core/sessions.py
# SentinelOps — DB-backed Session Helpers

from datetime import datetime, timedelta, timezone
from uuid import uuid4
from sqlalchemy.orm import Session as DBSession

from app.models.session import Session as SessionModel


SESSION_EXPIRE_HOURS = 12


# ------------------------------------------------------------
# Create a new session
# ------------------------------------------------------------
def create_session(db: DBSession, user_id: int) -> str:
    session_id = str(uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(hours=SESSION_EXPIRE_HOURS)

    db_session = SessionModel(
        id=session_id,
        user_id=user_id,
        expires_at=expires_at,
    )

    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    return session_id


# ------------------------------------------------------------
# Retrieve a session by ID
# ------------------------------------------------------------
def get_session_by_id(db: DBSession, session_id: str):
    return (
        db.query(SessionModel)
        .filter(SessionModel.id == session_id)
        .first()
    )


# ------------------------------------------------------------
# Delete a single session
# ------------------------------------------------------------
def delete_session(db: DBSession, session_id: str):
    session = get_session_by_id(db, session_id)
    if session:
        db.delete(session)
        db.commit()


# ------------------------------------------------------------
# NEW: Get all sessions for a user
# ------------------------------------------------------------
def get_sessions_for_user(db: DBSession, user_id: int):
    return (
        db.query(SessionModel)
        .filter(SessionModel.user_id == user_id)
        .order_by(SessionModel.expires_at.desc())
        .all()
    )


# ------------------------------------------------------------
# NEW: Delete all sessions for a user (single-session enforcement)
# ------------------------------------------------------------
def destroy_existing_sessions_for_user(db: DBSession, user_id: int):
    db.query(SessionModel).filter(
        SessionModel.user_id == user_id
    ).delete()
    db.commit()


# ------------------------------------------------------------
# NEW: Admin — list all sessions
# ------------------------------------------------------------
def get_all_sessions(db: DBSession):
    return (
        db.query(SessionModel)
        .order_by(SessionModel.expires_at.desc())
        .all()
    )
