import time
import secrets
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

SESSION_COOKIE_NAME = "session_id"
SESSION_TIMEOUT = 900  # 15 minutes inactivity timeout

# In-memory session store (replace with Redis in production)
SESSION_STORE = {}  # { session_id: { "user_id": ..., "last_seen": ... } }


class SessionManagerMiddleware(BaseHTTPMiddleware):
    """
    Hardened session middleware:
    - Enforces 15-minute inactivity timeout
    - No sliding renewal
    - Single active session per user (Option A)
    - Secure, HttpOnly cookie
    """

    def __init__(self, app, session_secret: str):
        # Accept session_secret so main.py can pass it
        super().__init__(app)
        self.session_secret = session_secret

    async def dispatch(self, request: Request, call_next):
        session_id = request.cookies.get(SESSION_COOKIE_NAME)
        now = int(time.time())

        # Attach session info to request.state
        request.state.session = None

        if session_id and session_id in SESSION_STORE:
            session = SESSION_STORE[session_id]

            # Check inactivity timeout
            if now - session["last_seen"] > SESSION_TIMEOUT:
                # Session expired
                del SESSION_STORE[session_id]
                response = await call_next(request)
                response.delete_cookie(
                    SESSION_COOKIE_NAME,
                    path="/",
                )
                return response

            # VALID SESSION → update last_seen (no sliding renewal)
            session["last_seen"] = now
            request.state.session = session

        response: Response = await call_next(request)

        # If login occurred, routers will set request.state.new_session
        if hasattr(request.state, "new_session"):
            user_id = request.state.new_session

            # Enforce single active session per user
            for sid, data in list(SESSION_STORE.items()):
                if data["user_id"] == user_id:
                    del SESSION_STORE[sid]

            # Create new session
            new_session_id = secrets.token_hex(32)
            SESSION_STORE[new_session_id] = {
                "user_id": user_id,
                "last_seen": now,
            }

            # Set cookie
            response.set_cookie(
                key=SESSION_COOKIE_NAME,
                value=new_session_id,
                max_age=SESSION_TIMEOUT,
                httponly=True,
                secure=True,
                samesite="none",
                path="/",
            )

        return response

