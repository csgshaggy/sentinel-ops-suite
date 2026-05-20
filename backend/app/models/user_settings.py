# backend/app/models/user_settings.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    display_name = Column(String, default="")
    landing_page = Column(String, default="dashboard")

    show_profile = Column(Boolean, default=True)
    show_clock = Column(Boolean, default=True)
    use_24h = Column(Boolean, default=False)
    show_seconds = Column(Boolean, default=False)
    show_day = Column(Boolean, default=False)

    sidebar_collapsed = Column(Boolean, default=False)
    enable_sounds = Column(Boolean, default=True)
    enable_toasts = Column(Boolean, default=True)

    auto_refresh = Column(Integer, default=0)

    timezone = Column(String, default="UTC")
    locale = Column(String, default="en-US")
    time_format = Column(String, default="24h")

    session_timeout = Column(Integer, default=900)
    auto_logout = Column(Boolean, default=True)
    reauth_sensitive = Column(Boolean, default=True)

    # ⭐ NEW — Theme Preferences
    theme_mode = Column(String, default="system")          # "light" | "dark" | "system"
    accent_color = Column(String, default="#4f46e5")       # Indigo-600 default

    user = relationship("User", back_populates="settings")
