# app/services/settings_service.py
# SentinelOps — User Settings Service

from sqlalchemy.orm import Session
from app.models.user import User


def get_settings(user: User) -> dict:
    """
    Return the current user's settings as a simple dict.
    """
    return {
        "theme": user.theme,
        "notifications": user.notifications,
    }


def update_settings(
    db: Session,
    user: User,
    theme: str | None = None,
    notifications: bool | None = None,
) -> dict:
    """
    Update the current user's settings and persist to the database.
    """
    if theme is not None:
        user.theme = theme

    if notifications is not None:
        user.notifications = notifications

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "theme": user.theme,
        "notifications": user.notifications,
    }
