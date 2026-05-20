from datetime import datetime, timedelta
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.session import SessionLocal
from src.session_models import Session as SessionModel


SESSION_TIMEOUT_MINUTES = 15


class SessionTimeoutMiddleware(BaseHTTPMiddleware):
    """
    Sliding session timeout middleware.

    - Reads session_id from cookie
    - Loads session from DB
    - Checks last_active timestamp
    - If expired → delete session + return 401
    - If valid → update last_active and continue
    """

    async def dispatch(self, request: Request, call_next):
        session_id = request.cookies.get("session_id")

        # No session cookie → proceed normally
        if not session_id:
            return await call_next(request)

        db = SessionLocal()
        try:
            session = (
                db.query(SessionModel)
                .filter(SessionModel.id == session_id)
                .first()
            )

            # Session not found → unauthorized
            if not session:
                return JSONResponse(status_code=401, content={"detail": "Session expired"})

            now = datetime.utcnow()
            last_active = session.last_active

            # Check expiration
            if now - last_active > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                db.delete(session)
                db.commit()
                return JSONResponse(status_code=401, content={"detail": "Session expired"})

            # Update sliding expiration
            session.last_active = now
            db.commit()

        finally:
            db.close()

        # Continue request
        return await call_next(request)
