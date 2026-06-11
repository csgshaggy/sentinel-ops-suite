# backend/app/api/routes/api_keys.py

from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.api_keys import (
  ApiKeyRead,
  ApiKeyCreate,
  ApiKeyCreateResponse,
)

router = APIRouter()


@router.get("/api-keys", response_model=List[ApiKeyRead])
async def list_api_keys():
  """
  List API keys for the current user.

  For now, returns an empty list so the frontend can render
  without crashing. Real data will be wired in later steps.
  """
  return []


@router.post(
  "/api-keys",
  response_model=ApiKeyCreateResponse,
  status_code=status.HTTP_201_CREATED,
)
async def create_api_key(payload: ApiKeyCreate):
  """
  Create a new API key.

  For now, this returns a stubbed key. In a later step we will:
    - generate a secure random key
    - hash it
    - store it in the database
    - return only the plaintext once
  """
  now = datetime.now(timezone.utc)
  return ApiKeyCreateResponse(
    id=1,
    name=payload.name,
    created_at=now,
    plaintext_key="STUB-KEY-REPLACE-IN-HASHING-STEP",
  )


@router.delete("/api-keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(key_id: int):
  """
  Revoke an API key.

  For now, this is a stub that always succeeds.
  Real revocation logic will be added in a later step.
  """
  return
