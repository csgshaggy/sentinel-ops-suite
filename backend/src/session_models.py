# /home/ubuntu/sentinel-ops-suite/backend/src/session_models.py

from datetime import datetime, timedelta
import secrets
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship, Session as DBSession

from app.db.base import Base  # canonical Base


# ---------------------------------------------------------------------------
# Session Model
# ---------------------------------------------------------------------------

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), unique=True, nullable=False, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_activity = Column(DateTime, default=datetime.utcnow, nullable=False)

    ip_address = Column(String(64), nullable=True)
    user_agent = Column(String(255), nullable=True)

    user = relationship("User", back_populates="sessions")


# ---------------------------------------------------------------------------
# Session Helper Functions
# ---------------------------------------------------------------------------

INACTIVITY_TIMEOUT_MINUTES = 15


def generate_session_id() -> str:
    """Generate a secure random session ID."""
    return secrets.token_hex(32)


def destroy_existing_sessions(db: DBSession, user_id: int) -> None:
    """Enforce single active session per user."""
    db.query(Session).filter(Session.user_id == user_id).delete()
    db.commit()


def create_session(
    db: DBSession,
    user_id: int,
    ip_address: str | None,
    user_agent: str | None,
) -> Session:
    """Create a new session for a user."""
    session = Session(
        session_id=generate_session_id(),
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session_by_id(db: DBSession, session_id: str) -> Session | None:
    """Retrieve a session by its session_id."""
    return (
        db.query(Session)
        .filter(Session.session_id == session_id)
        .first()
    )


def is_session_expired(session: Session) -> bool:
    """Check if a session is expired based on inactivity timeout."""
    now = datetime.utcnow()
    return now - session.last_activity > timedelta(minutes=INACTIVITY_TIMEOUT_MINUTES)


def update_last_activity(db: DBSession, session: Session) -> None:
    """Update last_activity timestamp."""
    session.last_activity = datetime.utcnow()
    db.commit()


def validate_session(db: DBSession, session_id: str) -> Session | None:
    """
    Validate a session:
    - Exists
    - Not expired
    - Updates last_activity (sliding timeout)
    """
    session = get_session_by_id(db, session_id)
    if not session:
        return None

    if is_session_expired(session):
        db.delete(session)
        db.commit()
        return None

    update_last_activity(db, session)
    return session


def destroy_session(db: DBSession, session_id: str) -> None:
    """Delete a session by session_id."""
    db.query(Session).filter(Session.session_id == session_id).delete()
    db.commit()
