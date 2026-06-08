## /app/routers/profile.py
## SentinelOps — Profile Router (Avatar Upload + Crop + Resize + History + Audit)

from fastapi import APIRouter, Depends, UploadFile, File, Request, HTTPException
from app.dependencies.auth import get_current_user_from_session
from app.db.session import get_db
from sqlalchemy.orm import Session

import os
import shutil
import logging
import uuid
from datetime import datetime
from typing import Optional
from PIL import Image

router = APIRouter()
logger = logging.getLogger("avatar")

# ------------------------------------------------------------
# Avatar Directories
# ------------------------------------------------------------

AVATAR_DIR = "static/avatars"
AVATAR_HISTORY_DIR = os.path.join(AVATAR_DIR, "history")

os.makedirs(AVATAR_DIR, exist_ok=True)
os.makedirs(AVATAR_HISTORY_DIR, exist_ok=True)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def _safe_ext(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".png", ".jpg", ".jpeg", ".webp"]:
        return ".png"
    return ext


def _center_crop_square(img: Image.Image) -> Image.Image:
    w, h = img.size
    side = min(w, h)

    left = (w - side) // 2
    top = (h - side) // 2

    return img.crop((left, top, left + side, top + side))


def _resize_avatar(img: Image.Image, size: int = 256) -> Image.Image:
    return img.resize((size, size), Image.LANCZOS)


def _archive_old_avatar(user):
    """
    Move existing avatar to history folder
    """
    if not user.avatar_url:
        return None

    current_path = user.avatar_url.lstrip("/")

    if not os.path.exists(current_path):
        return None

    ext = os.path.splitext(current_path)[1] or ".png"
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    history_filename = f"user_{user.id}_{timestamp}{ext}"
    history_path = os.path.join(AVATAR_HISTORY_DIR, history_filename)

    shutil.move(current_path, history_path)

    return f"/{history_path}"


def _log_avatar_event(
    user,
    action: str,
    request: Optional[Request] = None,
    extra: Optional[dict] = None,
):
    ip = request.client.host if request and request.client else None
    user_agent = request.headers.get("user-agent") if request else None

    payload = {
        "user_id": getattr(user, "id", None),
        "username": getattr(user, "username", None),
        "action": action,
        "ip": ip,
        "user_agent": user_agent,
        "extra": extra or {},
    }

    logger.info(f"avatar_event={payload}")

# ------------------------------------------------------------
# GET /profile
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# POST /profile/update
# ------------------------------------------------------------

@router.post("/profile/update")
async def update_profile(
    request: Request,
    data: dict,
    user=Depends(get_current_user_from_session),
    db: Session = Depends(get_db),
):
    user.email = data.get("email", user.email)
    user.username = data.get("username", user.username)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "status": "updated",
        "profile": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role,
            "mfa_enabled": user.mfa_enabled,
            "avatar_url": user.avatar_url,
        },
    }

# ------------------------------------------------------------
# POST /profile/avatar
# ------------------------------------------------------------

@router.post("/profile/avatar")
async def upload_avatar(
    request: Request,
    avatar: UploadFile = File(...),
    user=Depends(get_current_user_from_session),
    db: Session = Depends(get_db),
):
    allowed_types = {"image/png", "image/jpeg", "image/jpg", "image/webp"}

    if avatar.content_type not in allowed_types:
        _log_avatar_event(
            user,
            "upload_rejected_type",
            request,
            {"content_type": avatar.content_type},
        )
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Use PNG, JPG, or WEBP.",
        )

    ext = _safe_ext(avatar.filename or ".png")

    temp_filename = f"tmp_{user.id}_{uuid.uuid4().hex}{ext}"
    temp_path = os.path.join(AVATAR_DIR, temp_filename)

    final_filename = f"user_{user.id}{ext}"
    final_path = os.path.join(AVATAR_DIR, final_filename)

    try:
        # Save temp file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)

        # Process image
        with Image.open(temp_path) as img:
            # Normalize format
            if ext in [".png", ".webp"]:
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")

            img = _center_crop_square(img)
            img = _resize_avatar(img, 256)

            # Archive existing avatar before overwrite
            _archive_old_avatar(user)

            # Save final image
            save_format = "PNG"
            if ext in [".jpg", ".jpeg"]:
                save_format = "JPEG"
            elif ext == ".webp":
                save_format = "WEBP"

            img.save(final_path, format=save_format, quality=95)

        # Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # Update DB
        user.avatar_url = f"/{final_path}"

        db.add(user)
        db.commit()
        db.refresh(user)

        _log_avatar_event(
            user,
            "upload_success",
            request,
            {
                "avatar_url": user.avatar_url,
                "filename": avatar.filename,
            },
        )

        return {
            "status": "uploaded",
            "avatar_url": user.avatar_url,
        }

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)

        _log_avatar_event(
            user,
            "upload_failed",
            request,
            {"error": str(e)},
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to process avatar upload.",
        )

# ------------------------------------------------------------
# DELETE /profile/avatar
# ------------------------------------------------------------

@router.delete("/profile/avatar")
async def delete_avatar(
    request: Request,
    user=Depends(get_current_user_from_session),
    db: Session = Depends(get_db),
):
    if not user.avatar_url:
        _log_avatar_event(user, "delete_no_avatar", request)
        return {"status": "no_avatar"}

    avatar_path = user.avatar_url.lstrip("/")

    if os.path.exists(avatar_path):
        _archive_old_avatar(user)

    user.avatar_url = None

    db.add(user)
    db.commit()
    db.refresh(user)

    _log_avatar_event(user, "delete_success", request)

    return {"status": "deleted"}
