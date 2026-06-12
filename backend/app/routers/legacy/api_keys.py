# backend/app/routers/api_keys.py
# SentinelOps — API Keys Router (Create + Hash + Revoke)

from fastapi import APIRouter, Depends, HTTPException, Cookie, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import secrets
import hashlib

from app.db.session import get_db
from app.core.sessions import get_session_by_id

from app.schemas.api_keys import ApiKeyRead, ApiKeyCreate, ApiKeyCreateResponse

from app.services.api_key_service import (
    list_api_keys,
    get_api_key,
    create_api_key_record,
    revoke_api_key,
)

router = APIRouter(prefix="/api-keys", tags=["api-keys"])


# ------------------------------------------------------------
# Helper — authenticated user via session cookie
# ------------------------------------------------------------
def get_current_user_id_from_cookie(
    session_id: str | None,
    db: Session,
) -> int:
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = get_session_by_id(db, session_id)
    if not session or session.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired")

    return session.user_id


# ------------------------------------------------------------
# GET /api/auth/api-keys — list keys
# ------------------------------------------------------------
@router.get("", response_model=list[ApiKeyRead])
async def list_user_api_keys(
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id_from_cookie(session_id, db)
    return list_api_keys(db, user_id)


# ------------------------------------------------------------
# POST /api/auth/api-keys — create key
# ------------------------------------------------------------
@router.post(
    "",
    response_model=ApiKeyCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_api_key(
    payload: ApiKeyCreate,
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id_from_cookie(session_id, db)

    # Generate secure random plaintext key
    plaintext_key = "SOPS_" + secrets.token_urlsafe(32)

    # Hash with SHA-256
    key_hash = hashlib.sha256(plaintext_key.encode("utf-8")).hexdigest()

    # Persist record
    api_key = create_api_key_record(
        db=db,
        user_id=user_id,
        name=payload.name,
        key_hash=key_hash,
    )

    return ApiKeyCreateResponse(
        id=api_key.id,
        name=api_key.name,
        created_at=api_key.created_at,
        plaintext_key=plaintext_key,
    )


# ------------------------------------------------------------
# DELETE /api/auth/api-keys/{key_id} — revoke key
# ------------------------------------------------------------
@router.delete("/{key_id}")
async def delete_api_key(
    key_id: int,
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id_from_cookie(session_id, db)

    api_key = get_api_key(db, user_id, key_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")

    revoke_api_key(db, api_key)

    return {
        "success": True,
        "message": f"API key {key_id} revoked.",
    }
