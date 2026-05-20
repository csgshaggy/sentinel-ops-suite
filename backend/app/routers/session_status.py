from datetime import datetime
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session as DBSession

# Correct import for DB dependency
from app.dependencies.auth import get_db

# Correct session model import
from auth.models import Session as SessionModel

# Correct session helper imports
from app.utils.sessions import (
    _get_cookie,
    _fetch_session,
    _is_absolute_expired,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/session-status")
def session_status(request: Request, db: DBSession = Depends(get_db)):
    token = _get_cookie(request)
    if not token:
        raise HTTPException(status_code=401, detail="session_expired")

    sess = _fetch_session(db, token)
    if not sess:
        raise HTTPException(status_code=401, detail="session_expired")

    now = datetime.utcnow()

    # Absolute expiration
    if _is_absolute_expired(sess):
        raise HTTPException(status_code=401, detail="session_expired")

    # Hard expiration
    if sess.expires_at < now:
        raise HTTPException(status_code=401, detail="session_expired")

    # Sliding inactivity (your model uses last_activity_at)
    INACTIVITY_MINUTES = 15
    if sess.last_activity_at and sess.last_activity_at < now - timedelta(minutes=INACTIVITY_MINUTES):
        raise HTTPException(status_code=401, detail="session_expired")

    # Compute telemetry
    expires_in = int((sess.expires_at - now).total_seconds())

    # Your model does NOT have inactivity_delta or absolute_delta
    inactive_in = None
    absolute_in = None

    return {
        "valid": True,
        "expires_in": expires_in,
        "inactive_in": inactive_in,
        "absolute_in": absolute_in,
    }
