# /app/dependencies/auth.py
# SentinelOps — Authentication Dependencies (Session-Based Auth, RBAC)

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import SessionLocal
from auth.models import User, Session as SessionModel


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user_from_session(request: Request, db: Session = Depends(get_db)) -> User:
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    session = (
        db.query(SessionModel)
        .filter(SessionModel.id == session_id, SessionModel.is_active == True)
        .first()
    )

    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session")

    if session.expires_at < datetime.utcnow():
        session.is_active = False
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")

    user = db.query(User).filter(User.id == session.user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


def require_roles(*roles: str):
    def wrapper(user: User = Depends(get_current_user_from_session)):
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user

    return wrapper
