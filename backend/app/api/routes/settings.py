# backend/app/api/routes/settings.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.routers.auth import get_current_user
from app.dependencies import get_db
from app.models.user_settings import UserSettings
from app.schemas.settings import UserSettingsUpdate, UserSettingsOut

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("/", response_model=UserSettingsOut)
async def get_settings(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings = db.query(UserSettings).filter_by(user_id=user.id).first()
    return settings


@router.patch("/", response_model=UserSettingsOut)
async def update_settings(
    payload: UserSettingsUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings = db.query(UserSettings).filter_by(user_id=user.id).first()

    updates = payload.dict(exclude_unset=True)
    for key, value in updates.items():
        setattr(settings, key, value)

    db.commit()
    db.refresh(settings)
    return settings
