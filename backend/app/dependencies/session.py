# app/dependencies/session.py

from fastapi import Cookie, HTTPException, Depends
from sqlalchemy.orm import Session as DBSession

from app.db.session import get_db
from app.core.sessions import get_session_by_id


def require_session(
    session_id: str | None = Cookie(None),
    db: DBSession = Depends(get_db),
):
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = get_session_by_id(db, session_id)
    if not session or session.is_expired():
        raise HTTPException(status_code=401, detail="Session expired")

    return session
