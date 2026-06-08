# app/core/sessions.py
# SentinelOps — DB-backed Session Helpers

from datetime import datetime, timedelta, timezone
from uuid import uuid4
from sqlalchemy.orm import Session as DBSession

from app.models.session import Session as SessionModel


SESSION_EXPIRE_HOURS = 12


def create_session(db: DBSession, user_id: int) -> str:
    session_id = str(uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(hours=SESSION_EXPIRE_HOURS)

    db_session = SessionModel(
        id=session_id,          # <-- FIXED
        user_id=user_id,
        expires_at=expires_at,
    )

    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    return session_id


def get_session_by_id(db: DBSession, session_id: str):
    return (
        db.query(SessionModel)
        .filter(SessionModel.id == session_id)   # <-- FIXED
        .first()
    )


def delete_session(db: DBSession, session_id: str):
    session = get_session_by_id(db, session_id)
    if session:
        db.delete(session)
        db.commit()
