# app/models/user_preferences.py
# SentinelOps — User Preferences Model (1-to-1 with User)

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import Base


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)

    # 1-to-1 relationship with User
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # User settings
    theme = Column(String(20), nullable=False, default="dark")
    notifications = Column(Boolean, nullable=False, default=True)
    timezone = Column(String(50), nullable=True)
    language = Column(String(10), nullable=True)

    # Timestamps
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

    # Backref to User
    user = relationship("User", back_populates="preferences")

    def __repr__(self):
        return f"<UserPreferences user_id={self.user_id} theme={self.theme}>"
