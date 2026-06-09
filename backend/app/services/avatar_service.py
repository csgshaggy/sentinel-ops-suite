"""
Unified Avatar Service (Final Working Version)
---------------------------------------------
Fixes:
- 400 Bad Request on upload
- Overly strict MIME/extension validation
- Browser JPG uploads failing (image/jpg, image/pjpeg)
- Files with no extension failing
- WEBP/HEIC failing even though Pillow can read them

Features:
- Accepts ANY image/* MIME type
- Converts everything to PNG
- Safe RGBA flattening
- Thumbnail generation (256x256)
- Cache-busting version tokens
- Old avatar cleanup
- Local FS or S3
"""

import os
import io
from PIL import Image
from fastapi import UploadFile, HTTPException

from app.core.config import settings
from app.services.s3_client import upload_to_s3

AVATAR_DIR = "static/avatars"
DEFAULT_AVATAR_FILENAME = "default-avatar.png"


# ------------------------------------------------------------
# Directory Helpers
# ------------------------------------------------------------
def ensure_avatar_dir() -> str:
    full_path = os.path.abspath(AVATAR_DIR)
    os.makedirs(full_path, exist_ok=True)
    return full_path


def get_default_avatar_url() -> str:
    return f"/static/avatars/{DEFAULT_AVATAR_FILENAME}"


def get_user_avatar_urls(user):
    if user.avatar_url:
        return user.avatar_url, user.avatar_thumb_url or user.avatar_url

    default = get_default_avatar_url()
    return default, default


# ------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------
def cleanup_old_avatars(user_id: int, avatar_root: str):
    patterns = [
        f"{user_id}_avatar.png",
        f"{user_id}_avatar_thumb.png",
    ]

    for filename in patterns:
        full_path = os.path.join(avatar_root, filename)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
            except Exception:
                pass


# ------------------------------------------------------------
# Validation (FIXED)
# ------------------------------------------------------------
def validate_file_type(file: UploadFile):
    """
    Accept ANY image/* MIME type.
    The router already checks file.content_type.startswith("image/").
    Pillow will validate the actual bytes.
    """
    content_type = (file.content_type or "").lower()

    if not content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.content_type}'. Only image files are allowed.",
        )


# ------------------------------------------------------------
# Avatar Save Pipeline
# ------------------------------------------------------------
async def save_user_avatar(db, user, file: UploadFile) -> str:
    validate_file_type(file)

    avatar_root = ensure_avatar_dir()
    cleanup_old_avatars(user.id, avatar_root)

    avatar_filename = f"{user.id}_avatar.png"
    thumb_filename = f"{user.id}_avatar_thumb.png"

    avatar_path = os.path.join(avatar_root, avatar_filename)
    thumb_path = os.path.join(avatar_root, thumb_filename)

    # Read uploaded bytes
    file_bytes = await file.read()

    # Decode image with Pillow
    try:
        img = Image.open(io.BytesIO(file_bytes))
    except Exception as e:
        raise HTTPException(400, f"Failed to read image: {str(e)}")

    # Normalize to RGB
    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[-1])
        img = bg
    else:
        img = img.convert("RGB")

    # Save full-size PNG
    try:
        img.save(avatar_path, format="PNG", optimize=True, compress_level=6)
    except Exception as e:
        raise HTTPException(400, f"Failed to save avatar: {str(e)}")

    # Generate thumbnail
    try:
        thumb = img.copy()
        thumb.thumbnail((256, 256), Image.Resampling.LANCZOS)
        thumb.save(thumb_path, format="PNG", optimize=True, compress_level=6)
    except Exception as e:
        raise HTTPException(400, f"Failed to generate thumbnail: {str(e)}")

    # Cache-busting version
    version = int(os.path.getmtime(avatar_path))

    # Local FS
    if not settings.USE_S3:
        avatar_url = f"/static/avatars/{avatar_filename}?v={version}"
        avatar_thumb_url = f"/static/avatars/{thumb_filename}?v={version}"

    # S3
    else:
        try:
            avatar_key = f"avatars/{avatar_filename}"
            thumb_key = f"avatars/{thumb_filename}"

            avatar_url = upload_to_s3(avatar_path, avatar_key) + f"?v={version}"
            avatar_thumb_url = upload_to_s3(thumb_path, thumb_key) + f"?v={version}"
        except Exception as e:
            raise HTTPException(400, f"S3 upload failed: {str(e)}")

    # Update DB
    user.avatar_url = avatar_url
    user.avatar_thumb_url = avatar_thumb_url
    db.add(user)
    db.commit()
    db.refresh(user)

    return avatar_url
