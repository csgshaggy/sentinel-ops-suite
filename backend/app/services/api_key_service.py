# backend/app/services/api_key_service.py
# SentinelOps — API Key Service Layer

from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.api_key import ApiKey


def list_api_keys(db: Session, user_id: int):
    return (
        db.query(ApiKey)
        .filter(ApiKey.user_id == user_id)
        .order_by(ApiKey.created_at.desc())
        .all()
    )


def get_api_key(db: Session, user_id: int, key_id: int):
    return (
        db.query(ApiKey)
        .filter(ApiKey.id == key_id, ApiKey.user_id == user_id)
        .first()
    )


def create_api_key_record(db: Session, user_id: int, name: str, key_hash: str):
    api_key = ApiKey(
        user_id=user_id,
        name=name,
        key_hash=key_hash,
        created_at=datetime.now(timezone.utc),
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key


def revoke_api_key(db: Session, api_key: ApiKey):
    db.delete(api_key)
    db.commit()
