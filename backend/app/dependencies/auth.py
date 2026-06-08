# /app/dependencies/auth.py
# SentinelOps — Authentication Dependencies (Session-Based Auth)

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.auth.session import get_active_session
from app.models.user import User


# ---------------------------------------------------------
# Database session dependency
# ---------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------
# Retrieve the current authenticated user (or raise 401)
# ---------------------------------------------------------
def get_current_user_from_session(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    session = get_active_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


# ---------------------------------------------------------
# RBAC: Require specific roles
# ---------------------------------------------------------
def require_roles(*roles: str):
    def wrapper(user: User = Depends(get_current_user_from_session)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return wrapper
