# /app/services/session_service.py
# SentinelOps — Session Service (Sliding + Absolute Expiration)

from datetime import datetime
from sqlalchemy.orm import Session as DBSession

from app.models.session import Session
from app.models.user import User
from app.core.session_config import (
    generate_session_token,
    inactivity_timedelta,
    absolute_timedelta,
    SESSION_COOKIE_NAME,
)


class SessionService:
    """
    Centralized session management:
    - create
    - validate
    - sliding expiration
    - absolute expiration
    - kill / delete
    """

    # ---------------------------------------------------------
    # Create a new session
    # ---------------------------------------------------------
    @staticmethod
    def create_session(db: DBSession, user: User) -> Session:
        now = datetime.utcnow()

        sess = Session(
            id=generate_session_token(),
            user_id=user.id,
            created_at=now,
            last_seen=now,
            expires_at=now + absolute_timedelta(),
            is_active=True,
        )

        db.add(sess)
        db.commit()
        db.refresh(sess)

        return sess

    # ---------------------------------------------------------
    # Validate + apply sliding expiration
    # ---------------------------------------------------------
    @staticmethod
    def validate_and_slide(db: DBSession, token: str) -> User | None:
        sess = db.query(Session).filter(Session.id == token).first()
        if not sess:
            return None

        now = datetime.utcnow()

        # Hard expiration
        if now >= sess.expires_at:
            return None

        # Idle expiration (sliding)
        if now - sess.last_seen > inactivity_timedelta():
            return None

        # Explicit kill switch
        if not sess.is_active:
            return None

        # Sliding update
        sess.last_seen = now
        db.commit()

        # 🔥 FIX: manually load user
        return db.query(User).filter(User.id == sess.user_id).first()

    # ---------------------------------------------------------
    # Validate without sliding (used by restore, heartbeat)
    # ---------------------------------------------------------
    @staticmethod
    def validate_no_slide(db: DBSession, token: str) -> User | None:
        sess = db.query(Session).filter(Session.id == token).first()
        if not sess:
            return None

        now = datetime.utcnow()

        if now >= sess.expires_at:
            return None

        if now - sess.last_seen > inactivity_timedelta():
            return None

        if not sess.is_active:
            return None

        # 🔥 FIX: manually load user
        return db.query(User).filter(User.id == sess.user_id).first()

    # ---------------------------------------------------------
    # Kill a session (logout)
    # ---------------------------------------------------------
    @staticmethod
    def kill_session(db: DBSession, token: str) -> bool:
        sess = db.query(Session).filter(Session.id == token).first()
        if not sess:
            return False

        sess.is_active = False
        db.commit()
        return True

    # ---------------------------------------------------------
    # Delete a session entirely
    # ---------------------------------------------------------
    @staticmethod
    def delete_session(db: DBSession, token: str) -> bool:
        sess = db.query(Session).filter(Session.id == token).first()
        if not sess:
            return False

        db.delete(sess)
        db.commit()
        return True

    # ---------------------------------------------------------
    # Restore session (no sliding)
    # ---------------------------------------------------------
    @staticmethod
    def restore(db: DBSession, token: str):
        sess = db.query(Session).filter(Session.id == token).first()
        if not sess:
            return None

        now = datetime.utcnow()

        if now >= sess.expires_at:
            return None

        if now - sess.last_seen > inactivity_timedelta():
            return None

        if not sess.is_active:
            return None

        # 🔥 FIX: manually load user
        user = db.query(User).filter(User.id == sess.user_id).first()
        if not user:
            return None

        return {
            "session_token": sess.id,
            "user": {
                "id": user.id,
                "username": user.username,
            },
        }
