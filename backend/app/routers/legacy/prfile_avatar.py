from typing import Any

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import SessionLocal

from app.models.user import User
from app.schemas.user import UserProfileResponse

# ✅ Correct import — THIS is your real avatar pipeline
from app.services.avatar_service import save_user_avatar


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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

    # Avatar service handles validation, cleanup, thumbnail, DB update
    await save_user_avatar(db, current_user, file)

    return current_user
