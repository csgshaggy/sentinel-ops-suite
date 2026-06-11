# backend/app/services/settings_service.py

from sqlalchemy.orm import Session
from app.models.user_settings import UserSettings
from app.schemas.settings import UserSettingsUpdate


def get_settings(db: Session, user_id: int) -> UserSettings:
    """
    Fetch settings for a user.
    If the user has no settings row yet, create one with defaults.
    """
    settings = (
        db.query(UserSettings)
        .filter(UserSettings.user_id == user_id)
        .first()
    )

    if not settings:
        settings = UserSettings(user_id=user_id)
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings


def update_settings(
    db: Session,
    user_id: int,
    updates: UserSettingsUpdate
) -> UserSettings:
    """
    Apply partial updates to the user's settings.
    Only fields explicitly provided will be updated.
    """
    settings = get_settings(db, user_id)

    update_data = updates.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(settings, field, value)

    db.commit()
    db.refresh(settings)

    return settings
