# backend/app/api/routes/settings.py
# SentinelOps — Unified User Settings Router (DB-backed sessions)

from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

from app.core.sessions import get_session_by_id
from app.db.session import get_db
from app.models.user_settings import UserSettings
from app.models.user import User
from app.schemas.settings import UserSettingsUpdate, UserSettingsOut

router = APIRouter(prefix="/api/settings", tags=["settings"])


# ------------------------------------------------------------
# Internal helper — resolve authenticated user
# ------------------------------------------------------------
def get_authenticated_user(
    session_id: str | None,
    db: Session
) -> User:
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = get_session_by_id(db, session_id)
    if not session or session.expires_at <= session.expires_at.utcnow():
        raise HTTPException(status_code=401, detail="Session expired")

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ------------------------------------------------------------
# GET /api/settings
# ------------------------------------------------------------
@router.get("/", response_model=UserSettingsOut)
async def get_settings(
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user = get_authenticated_user(session_id, db)

    settings = (
        db.query(UserSettings)
        .filter(UserSettings.user_id == user.id)
        .first()
    )

    # Auto-create settings row if missing
    if not settings:
        settings = UserSettings(user_id=user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings


# ------------------------------------------------------------
# PATCH /api/settings
# ------------------------------------------------------------
@router.patch("/", response_model=UserSettingsOut)
async def update_settings(
    payload: UserSettingsUpdate,
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user = get_authenticated_user(session_id, db)

    settings = (
        db.query(UserSettings)
        .filter(UserSettings.user_id == user.id)
        .first()
    )

    if not settings:
        settings = UserSettings(user_id=user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)

    updates = payload.dict(exclude_unset=True)
    for key, value in updates.items():
        setattr(settings, key, value)

    db.commit()
    db.refresh(settings)

    return settings
