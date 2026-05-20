from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class SessionLoaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session_id = request.cookies.get("sentinel_session")

        # Always initialize
        request.state.session = None

        if session_id:
            try:
                session = await request.app.state.session_store.get(session_id)
                if session:
                    request.state.session = session
            except Exception:
                # Never break the request chain
                request.state.session = None

        return await call_next(request)
