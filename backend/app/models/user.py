# SentinelOps — Unified User Model
# (MFA + Sessions + Preferences + Settings + Public Dict + Avatar Versioning)

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import Base

# ------------------------------------------------------------
# Ensure proper import order to avoid mapper issues
# ------------------------------------------------------------
from app.models.user_preferences import UserPreferences
from app.models.session import Session
from app.models.api_key import ApiKey


class User(Base):
    __tablename__ = "users"

    # ------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)

    # ------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)

    # ------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------
    password_hash = Column(String(255), nullable=False)

    # ------------------------------------------------------------
    # RBAC
    # ------------------------------------------------------------
    role = Column(String(50), nullable=False, default="user")

    # ------------------------------------------------------------
    # MFA
    # ------------------------------------------------------------
    mfa_enabled = Column(Boolean, default=False, nullable=False)
    mfa_secret = Column(String(255), nullable=True)

    # ------------------------------------------------------------
    # ✅ NEW: User Settings (persisted)
    # ------------------------------------------------------------
    theme = Column(String(20), nullable=False, default="dark")
    notifications = Column(Boolean, nullable=False, default=True)

    # ------------------------------------------------------------
    # Avatar (URL + Thumbnail + Version)
    # ------------------------------------------------------------
    avatar_url = Column(String(255), nullable=True)
    avatar_thumb_url = Column(String(255), nullable=True)

    # Cache-busting version for avatars
    avatar_version = Column(Integer, nullable=False, default=1)

    # ------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------

    # Sessions
    sessions = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # API Keys
    api_keys = relationship(
        "ApiKey",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # User Preferences (1-to-1)
    preferences = relationship(
        "UserPreferences",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # ------------------------------------------------------------
    # Public dict (used across frontend/auth)
    # ------------------------------------------------------------
    def to_public_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "mfa_enabled": self.mfa_enabled,
            "avatar_url": self.avatar_url,
            "avatar_thumb_url": self.avatar_thumb_url,
            "avatar_version": self.avatar_version,

            # ✅ NEW: expose settings
            "theme": self.theme,
            "notifications": self.notifications,
        }

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} role={self.role}>"
