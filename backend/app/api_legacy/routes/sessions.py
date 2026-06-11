# backend/app/api/routes/sessions.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.schemas.sessions import SessionRead, SessionTerminateResponse

router = APIRouter()


@router.get("/sessions", response_model=List[SessionRead])
async def list_sessions():
  """
  List active sessions for the current user.

  For now, returns an empty list so the frontend can render
  without crashing. Will be wired to real data in later steps.
  """
  return []


@router.delete("/sessions/{session_id}", response_model=SessionTerminateResponse)
async def terminate_session(session_id: str):
  """
  Terminate a specific session.

  For now, this is a stub that always reports success.
  Real termination logic will be added in a later step.
  """
  return SessionTerminateResponse(
    success=True,
    message=f"Session {session_id} termination stubbed (no-op).",
  )
