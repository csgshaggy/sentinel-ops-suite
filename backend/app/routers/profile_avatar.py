from typing import Any

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

# ✅ Correct import — this is where we will define get_current_user
from app.auth.dependencies import get_current_user

# DB session
from app.db.session import SessionLocal

from app.models.user import User
from app.schemas.user import UserProfileResponse
from app.services.storage import save_avatar_file, delete_avatar_file


# Local DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# NOTE: main.py mounts this router at /api/users/me
router = APIRouter(tags=["profile"])


@router.get("", response_model=UserProfileResponse)
def get_me_profile(
    current_user: User = Depends(get_current_user),
) -> Any:
    return current_user


@router.post("/avatar", response_model=UserProfileResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file.")

    # Delete old avatar if present
    if current_user.avatar_url:
        delete_avatar_file(current_user.avatar_url)
    if current_user.avatar_thumb_url:
        delete_avatar_file(current_user.avatar_thumb_url)

    # Save new avatar
    avatar_url, avatar_thumb_url = await save_avatar_file(
        file=file,
        user_id=current_user.id,
    )

    current_user.avatar_url = avatar_url
    current_user.avatar_thumb_url = avatar_thumb_url
    current_user.avatar_version = (current_user.avatar_version or 0) + 1

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return current_user
