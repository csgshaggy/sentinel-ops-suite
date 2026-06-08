"""
Unified Avatar Service (Final Corrected Version)
-----------------------------------------------
Supports:
- Local FS storage (static/avatars)
- Optional S3 storage
- PNG/JPG validation
- Safe RGBA flattening
- Thumbnail generation (256x256)
- Cache-busting version tokens
- Old avatar cleanup
"""

import os
import io
from PIL import Image
from fastapi import UploadFile, HTTPException

from app.core.config import settings
from app.services.s3_client import upload_to_s3

# Static directory (FastAPI mounts /static → ./static)
AVATAR_DIR = "static/avatars"
DEFAULT_AVATAR_FILENAME = "default-avatar.png"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg"}


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
    """
    Returns (avatar_url, avatar_thumb_url) with fallback to default avatar.
    """
    if user.avatar_url:
        return user.avatar_url, user.avatar_thumb_url or user.avatar_url

    default_url = get_default_avatar_url()
    return default_url, default_url


# ------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------
def cleanup_old_avatars(user_id: int, avatar_root: str):
    """
    Removes old avatar and thumbnail files for a given user.
    """
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
                pass  # Never break upload flow


# ------------------------------------------------------------
# Validation
# ------------------------------------------------------------
def validate_file_type(file: UploadFile):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PNG and JPG/JPEG are allowed.",
        )

    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file extension. Only PNG and JPG/JPEG are allowed.",
        )


# ------------------------------------------------------------
# Avatar Save Pipeline
# ------------------------------------------------------------
async def save_user_avatar(db, user, file: UploadFile) -> str:
    """
    Saves the uploaded avatar and generates a 256x256 thumbnail.
    Supports local FS or S3 depending on USE_S3.
    Returns: avatar_url (string)
    """

    # Step 1: Validate file type
    validate_file_type(file)

    # Step 2: Ensure directory exists
    avatar_root = ensure_avatar_dir()

    # Step 3: Cleanup old files
    cleanup_old_avatars(user.id, avatar_root)

    # Step 4: Filenames
    avatar_filename = f"{user.id}_avatar.png"
    thumb_filename = f"{user.id}_avatar_thumb.png"

    avatar_path = os.path.join(avatar_root, avatar_filename)
    thumb_path = os.path.join(avatar_root, thumb_filename)

    # Step 5: Read file into memory
    file_bytes = await file.read()

    # Save original
    with open(avatar_path, "wb") as f:
        f.write(file_bytes)

    # Step 6: Load image safely
    try:
        img = Image.open(io.BytesIO(file_bytes))
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read image: {str(e)}"
        )

    # Step 7: Flatten RGBA → RGB
    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    else:
        img = img.convert("RGB")

    # Step 8: Generate thumbnail
    try:
        img.thumbnail((256, 256), Image.Resampling.LANCZOS)
        img.save(
            thumb_path,
            format="PNG",
            optimize=True,
            compress_level=6,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate thumbnail: {str(e)}"
        )

    # Step 9: Cache-busting version token
    version = int(os.path.getmtime(avatar_path))

    # ------------------------------------------------------------
    # LOCAL FS MODE
    # ------------------------------------------------------------
    if not settings.USE_S3:
        avatar_url = f"/static/avatars/{avatar_filename}?v={version}"
        avatar_thumb_url = f"/static/avatars/{thumb_filename}?v={version}"

    # ------------------------------------------------------------
    # S3 MODE
    # ------------------------------------------------------------
    else:
        avatar_key = f"avatars/{avatar_filename}"
        thumb_key = f"avatars/{thumb_filename}"

        try:
            avatar_url = upload_to_s3(avatar_path, avatar_key) + f"?v={version}"
            avatar_thumb_url = upload_to_s3(thumb_path, thumb_key) + f"?v={version}"
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"S3 upload failed: {str(e)}"
            )

    # Step 12: Update DB
    user.avatar_url = avatar_url
    user.avatar_thumb_url = avatar_thumb_url
    db.add(user)
    db.commit()
    db.refresh(user)

    return avatar_url

