"""
Unified Avatar Service (Final Working Version + DEBUG)
------------------------------------------------------
Adds:
- Debug logging for every stage
- Full exception tracing
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
# Validation
# ------------------------------------------------------------
def validate_file_type(file: UploadFile):
    content_type = (file.content_type or "").lower()

    if not content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.content_type}'. Only image files are allowed.",
        )


# ------------------------------------------------------------
# Avatar Save Pipeline (DEBUG ENABLED)
# ------------------------------------------------------------
async def save_user_avatar(db, user, file: UploadFile) -> str:
    print("DEBUG: save_user_avatar called")
    print("DEBUG: filename =", file.filename)
    print("DEBUG: content_type =", file.content_type)

    try:
        # Step 1: Validate
        print("DEBUG: validating file type…")
        validate_file_type(file)

        # Step 2: Ensure directory
        print("DEBUG: ensuring avatar directory…")
        avatar_root = ensure_avatar_dir()

        # Step 3: Cleanup
        print("DEBUG: cleaning up old avatars…")
        cleanup_old_avatars(user.id, avatar_root)

        # Step 4: Paths
        avatar_filename = f"{user.id}_avatar.png"
        thumb_filename = f"{user.id}_avatar_thumb.png"

        avatar_path = os.path.join(avatar_root, avatar_filename)
        thumb_path = os.path.join(avatar_root, thumb_filename)

        # Step 5: Read bytes
        print("DEBUG: reading uploaded bytes…")
        file_bytes = await file.read()
        print("DEBUG: byte length =", len(file_bytes))

        # Step 6: Decode
        print("DEBUG: decoding image with Pillow…")
        img = Image.open(io.BytesIO(file_bytes))

        # Step 7: Normalize
        print("DEBUG: normalizing image mode =", img.mode)
        if img.mode in ("RGBA", "LA"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        else:
            img = img.convert("RGB")

        # Step 8: Save full PNG
        print("DEBUG: saving full-size PNG to", avatar_path)
        img.save(avatar_path, format="PNG", optimize=True, compress_level=6)

        # Step 9: Thumbnail
        print("DEBUG: generating thumbnail…")
        thumb = img.copy()
        thumb.thumbnail((256, 256), Image.Resampling.LANCZOS)
        thumb.save(thumb_path, format="PNG", optimize=True, compress_level=6)

        # Step 10: Version
        version = int(os.path.getmtime(avatar_path))
        print("DEBUG: version token =", version)

        # Step 11: URL generation
        if not settings.USE_S3:
            avatar_url = f"/static/avatars/{avatar_filename}?v={version}"
            avatar_thumb_url = f"/static/avatars/{thumb_filename}?v={version}"
        else:
            print("DEBUG: uploading to S3…")
            avatar_key = f"avatars/{avatar_filename}"
            thumb_key = f"avatars/{thumb_filename}"

            avatar_url = upload_to_s3(avatar_path, avatar_key) + f"?v={version}"
            avatar_thumb_url = upload_to_s3(thumb_path, thumb_key) + f"?v={version}"

        # Step 12: DB update
        print("DEBUG: updating DB user record…")
        user.avatar_url = avatar_url
        user.avatar_thumb_url = avatar_thumb_url
        db.add(user)
        db.commit()
        db.refresh(user)

        print("DEBUG: avatar upload completed successfully")
        return avatar_url

    except Exception as e:
        print("DEBUG: Avatar upload FAILED:", str(e))
        raise
