# /app/core/session_middleware.py
# SentinelOps — Session Middleware (Sliding Expiration)

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
from sqlalchemy.orm import Session as DBSession

from app.core.session_config import SESSION_COOKIE_NAME
from app.services.session_service import SessionService


class SessionMiddleware(BaseHTTPMiddleware):
    """
    Enforces session validation + sliding expiration on authenticated routes.

    Behavior:
    - Public routes bypass session checks
    - Authenticated routes require a valid session
    - Sliding expiration updates last_seen
    """

    def __init__(self, app, public_paths: list[str] | None = None):
        super().__init__(app)
        self.public_paths = public_paths or [
            "/api/auth/login",
            "/api/auth/restore",
            "/api/auth/heartbeat",
            "/api/auth/logout",
            "/docs",
            "/openapi.json",
        ]

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # ---------------------------------------------------------
        # 1. Public routes bypass session validation
        # ---------------------------------------------------------
        if any(path.startswith(p) for p in self.public_paths):
            return await call_next(request)

        # ---------------------------------------------------------
        # 2. Extract session token
        # ---------------------------------------------------------
        token = request.cookies.get(SESSION_COOKIE_NAME)
        if not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing session token"},
            )

        # ---------------------------------------------------------
        # 3. Validate + sliding expiration
        # ---------------------------------------------------------
        db: DBSession = request.state.db

        user = SessionService.validate_and_slide(db, token)
        if not user:
            return JSONResponse(
                status_code=401,
                content={"detail": "Session expired or invalid"},
            )

        # Attach user to request for downstream handlers
        request.state.user = user

        # ---------------------------------------------------------
        # 4. Continue request
        # ---------------------------------------------------------
        return await call_next(request)
