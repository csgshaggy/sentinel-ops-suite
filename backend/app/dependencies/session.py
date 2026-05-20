# File: app/dependencies/session.py

from typing import Optional, Any
from fastapi import Request


def get_current_session(request: Request) -> Optional[Any]:
    """
    Minimal session accessor used by dashboard and other routers.
    Returns the underlying Starlette session dict or None.
    """
    return getattr(request, "session", None)
