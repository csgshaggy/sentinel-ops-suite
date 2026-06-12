# app/services/avatar_service.py
# SentinelOps — Avatar Upload + Versioning + URL Helpers

import uuid
from datetime import datetime, timezone
from pathlib import Path

from app.models.user import User
from app.db.session import SessionLocal
from app.services.s3_client import s3


BUCKET_NAME = "sentinelops-avatars"


def _generate_avatar_key(user_id: int, version: int) -> str:
    return f"avatars/{user_id}/avatar_v{version}.png"


def save_user_avatar(user: User, file_bytes: bytes, content_type: str) -> None:
    """
    Uploads a new avatar to S3, bumps version, updates user record.
    """

    db = SessionLocal()

    # bump version
    user.avatar_version += 1
    version = user.avatar_version

    key = _generate_avatar_key(user.id, version)

    # upload to S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=file_bytes,
        ContentType=content_type,
        ACL="public-read",
    )

    # update URLs
    user.avatar_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
    user.avatar_thumb_url = user.avatar_url  # placeholder if no thumbnail pipeline

    user.updated_at = datetime.now(timezone.utc)

    db.add(user)
    db.commit()
    db.refresh(user)


def get_user_avatar_urls(user: User) -> dict:
    """
    Returns the current avatar URLs for the user.
    """
    return {
        "avatar_url": user.avatar_url,
        "avatar_thumb_url": user.avatar_thumb_url,
        "avatar_version": user.avatar_version,
    }
