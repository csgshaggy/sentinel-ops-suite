# backend/app/routers/settings_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user

from app.schemas.settings import UserSettingsOut, UserSettingsUpdate
from app.services.settings_service import get_settings, update_settings

router = APIRouter(
    prefix="/api/settings",
    tags=["settings"]
)


@router.get("/", response_model=UserSettingsOut)
def read_settings(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Return the unified settings object for the authenticated user.
    Automatically creates a settings row if missing.
    """
    return get_settings(db, user.id)


@router.put("/", response_model=UserSettingsOut)
def write_settings(
    updates: UserSettingsUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Apply partial updates to the user's settings.
    Only fields explicitly provided will be updated.
    """
    return update_settings(db, user.id, updates)
