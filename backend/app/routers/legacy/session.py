# /home/ubuntu/sentinel-ops-suite/backend/app/routers/session.py
# SentinelOps — Session Router (Async SQLAlchemy, MySQL Edition, Corrected Prefix)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
import secrets

from app.database import get_db
from src.session_models import Session
from app.schemas.session import SessionCreate, SessionRead

# ---------------------------------------------------------
# FIXED: Session router prefix corrected (no /api here)
# main.py applies prefix="/api"
# Final path becomes /api/sessions/*
# ---------------------------------------------------------
router = APIRouter(prefix="/sessions", tags=["Sessions"])


# ---------------------------------------------------------
# Create a New Session (after successful login)
# ---------------------------------------------------------
@router.post("/", response_model=SessionRead, status_code=201)
async def create_session(
    payload: SessionCreate,
    db: AsyncSession = Depends(get_db),
):
    # Generate a secure random session token
    session_token = secrets.token_urlsafe(48)

    session = Session(
        user_id=payload.user_id,
        session_token=session_token,
        user_agent=payload.user_agent,
        ip_address=payload.ip_address,
        expires_at=payload.expires_at,
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)

    return session


# ---------------------------------------------------------
# List All Sessions for a User
# ---------------------------------------------------------
@router.get("/user/{user_id}", response_model=list[SessionRead])
async def list_user_sessions(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Session).where(Session.user_id == user_id)
    result = await db.execute(stmt)
    sessions = result.scalars().all()
    return sessions


# ---------------------------------------------------------
# Invalidate a Session
# ---------------------------------------------------------
@router.delete("/{session_id}", status_code=204)
async def delete_session(session_id: int, db: AsyncSession = Depends(get_db)):
    stmt = delete(Session).where(Session.id == session_id)
    await db.execute(stmt)
    await db.commit()
    return


# ---------------------------------------------------------
# Admin: List All Sessions
# ---------------------------------------------------------
@router.get("/", response_model=list[SessionRead])
async def list_all_sessions(db: AsyncSession = Depends(get_db)):
    stmt = select(Session)
    result = await db.execute(stmt)
    sessions = result.scalars().all()
    return sessions

