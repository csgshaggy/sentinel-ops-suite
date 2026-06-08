# /app/routers/session_status.py
# SentinelOps — Session Status Router (Sliding-Ready)

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session as DBSession

from app.db.session import get_db
from app.services.session_service import SessionService
from app.core.session_config import SESSION_COOKIE_NAME


router = APIRouter(prefix="/api/auth", tags=["auth"])


# ---------------------------------------------------------
# SESSION STATUS (Frontend uses this to check auth)
# ---------------------------------------------------------
@router.get("/session-status")
def session_status(request: Request, db: DBSession = Depends(get_db)):
    token = request.cookies.get(SESSION_COOKIE_NAME)

    if not token:
        return {"active": False}

    # No sliding here — middleware handles sliding for protected routes
    user = SessionService.validate_no_slide(db, token)

    return {"active": bool(user)}
