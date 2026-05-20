# /app/routers/users.py
# SentinelOps — Users Router (Sync SQLAlchemy, Session-Based Auth)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.models import User
from app.dependencies.auth import get_db, require_roles, get_current_user_from_session

router = APIRouter(tags=["users"])


# ---------------------------------------------------------
# Get current user
# ---------------------------------------------------------
@router.get("/me")
def get_me(user: User = Depends(get_current_user_from_session)):
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }


# ---------------------------------------------------------
# List all users (admin only)
# ---------------------------------------------------------
@router.get("/")
def list_users(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),
):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "role": u.role,
            "is_active": u.is_active,
        }
        for u in users
    ]


# ---------------------------------------------------------
# Get user by ID (admin only)
# ---------------------------------------------------------
@router.get("/{user_id}")
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),
):
    user_obj = db.query(User).filter(User.id == user_id).first()

    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user_obj.id,
        "email": user_obj.email,
        "role": user_obj.role,
        "is_active": user_obj.is_active,
    }
