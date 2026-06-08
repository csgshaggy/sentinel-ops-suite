from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.user_preferences import UserPreferences
from app.schemas.user_preferences import AdminUpdatePreferences
from app.core.security import admin_required

router = APIRouter()

# ------------------------------------------------------------
# GET ALL USER PREFERENCES
# ------------------------------------------------------------
@router.get("/user-preferences")
def get_all_user_preferences(
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    """
    Returns all users + their preference rows.
    Ensures admin-only access.
    """

    users = (
        db.query(User, UserPreferences)
        .join(UserPreferences, User.id == UserPreferences.user_id)
        .all()
    )

    return [
        {
            "user_id": u.id,
            "username": u.username,
            "theme": p.theme,
            "accent": p.accent,
            "timezone": p.timezone,
            "language": p.language,
            "login_alerts": p.login_alerts,
            "security_warnings": p.security_warnings,
            "product_updates": p.product_updates,
            "session_timeout": p.session_timeout,
        }
        for u, p in users
    ]


# ------------------------------------------------------------
# UPDATE A SINGLE USER'S PREFERENCES
# ------------------------------------------------------------
@router.put("/user-preferences/{user_id}")
def update_user_preferences(
    user_id: int,
    prefs: AdminUpdatePreferences,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    """
    Updates a single user's preferences.
    Validates fields via AdminUpdatePreferences schema.
    """

    record = (
        db.query(UserPreferences)
        .filter(UserPreferences.user_id == user_id)
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="User preferences not found")

    # Apply validated fields
    update_data = prefs.dict()

    for field, value in update_data.items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)

    return {
        "status": "success",
        "updated_user_id": record.user_id,
        "updated_fields": update_data
    }
