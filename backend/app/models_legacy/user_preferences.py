# app/models/user_preferences.py
# SentinelOps — User Preferences Model (1-to-1 with User)

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)

    # 1-to-1 FK to User
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    # ------------------------------------------------------------
    # UI Preferences
    # ------------------------------------------------------------
    theme = Column(String, default="system")     # system | dark | light | neon
    accent = Column(String, default="cyan")      # cyan | blue | purple | green | red

    # ------------------------------------------------------------
    # Localization
    # ------------------------------------------------------------
    timezone = Column(String, default="UTC")
    language = Column(String, default="en")

    # ------------------------------------------------------------
    # Notifications
    # ------------------------------------------------------------
    login_alerts = Column(Boolean, default=True)
    security_warnings = Column(Boolean, default=True)
    product_updates = Column(Boolean, default=False)

    # ------------------------------------------------------------
    # Session Behavior
    # ------------------------------------------------------------
    session_timeout = Column(Integer, default=15)

    # ------------------------------------------------------------
    # Relationship back to User
    # ------------------------------------------------------------
    user = relationship("User", back_populates="preferences")
