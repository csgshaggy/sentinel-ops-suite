# app/models/session.py
# SentinelOps — Unified DB Session Model (Refactored + Production-Ready)

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Session(Base):
    __tablename__ = "sessions"

    # ------------------------------------------------------------
    # Primary Key — UUID (Fixes NULL identity key issue)
    # ------------------------------------------------------------
    id = Column(
        String(36),  # UUID length
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),  # ✅ FIX: auto-generate ID
    )

    # ------------------------------------------------------------
    # Foreign Keys
    # ------------------------------------------------------------
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # ------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    # ------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------
    user = relationship(
        "User",
        back_populates="sessions",
        lazy="joined",  # eager load for auth performance
    )

    # ------------------------------------------------------------
    # Utility Methods
    # ------------------------------------------------------------
    def is_expired(self) -> bool:
        """
        Determine if the session is expired.

        Ensures timezone-safe comparison.
        """
        if not self.expires_at:
            return True

        expires = self.expires_at

        # Normalize naive timestamps → UTC
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)

        return datetime.now(timezone.utc) >= expires

    def to_dict(self) -> dict:
        """
        Serialize session for API responses or logging.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_expired": self.is_expired(),
        }

    def __repr__(self) -> str:
        return f"<Session id={self.id} user_id={self.user_id} expires_at={self.expires_at}>"
