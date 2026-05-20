# /app/routers/profile.py

from fastapi import APIRouter, Depends, UploadFile, File, Request
from app.dependencies.auth import get_current_user_from_session
from app.db.session import get_db
import os
import shutil

router = APIRouter()

AVATAR_DIR = "static/avatars"
os.makedirs(AVATAR_DIR, exist_ok=True)


@router.get("/profile")
async def get_profile(
    request: Request,
    user=Depends(get_current_user_from_session),
):
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "role": user.role,
        "mfa_enabled": user.mfa_enabled,
        "avatar_url": user.avatar_url,
    }


@router.post("/profile/update")
async def update_profile(
    request: Request,
    data: dict,
    user=Depends(get_current_user_from_session),
    db=Depends(get_db),
):
    user.email = data.get("email", user.email)
    user.username = data.get("username", user.username)

    db.add(user)
    db.commit()

    return {"status": "ok"}


@router.post("/profile/avatar")
async def upload_avatar(
    request: Request,
    avatar: UploadFile = File(...),
    user=Depends(get_current_user_from_session),
    db=Depends(get_db),
):
    filename = f"user_{user.id}.png"
    filepath = os.path.join(AVATAR_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(avatar.file, buffer)

    user.avatar_url = f"/static/avatars/{filename}"
    db.add(user)
    db.commit()

    return {"avatar_url": user.avatar_url}
