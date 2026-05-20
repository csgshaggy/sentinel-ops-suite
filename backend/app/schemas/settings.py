# backend/app/schemas/settings.py

from pydantic import BaseModel
from typing import Optional

class UserSettingsBase(BaseModel):
    display_name: Optional[str] = None
    landing_page: Optional[str] = None

    show_profile: Optional[bool] = None
    show_clock: Optional[bool] = None
    use_24h: Optional[bool] = None
    show_seconds: Optional[bool] = None
    show_day: Optional[bool] = None

    sidebar_collapsed: Optional[bool] = None
    enable_sounds: Optional[bool] = None
    enable_toasts: Optional[bool] = None

    auto_refresh: Optional[int] = None

    timezone: Optional[str] = None
    locale: Optional[str] = None
    time_format: Optional[str] = None

    session_timeout: Optional[int] = None
    auto_logout: Optional[bool] = None
    reauth_sensitive: Optional[bool] = None

    # ⭐ NEW — Theme Preferences
    theme_mode: Optional[str] = None
    accent_color: Optional[str] = None


class UserSettingsUpdate(UserSettingsBase):
    """
    Accepts partial updates.
    All fields optional.
    """
    pass


class UserSettingsOut(UserSettingsBase):
    user_id: int

    class Config:
        orm_mode = True
