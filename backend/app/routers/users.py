# backend/app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter(prefix="/users", tags=["users"])


# ---------------------------------------------------------------------------
# CURRENT USER DEPENDENCY
# ---------------------------------------------------------------------------

def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> models.User:
    """
    Validate the session and return the authenticated user.
    """

    user_id = request.session.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


# ---------------------------------------------------------------------------
# /users/me
# ---------------------------------------------------------------------------

@router.get("/me")
async def read_me(current_user: models.User = Depends(get_current_user)):
    """
    Return the authenticated user's profile.
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "is_active": current_user.is_active,
    }


# ---------------------------------------------------------------------------
# /users/{user_id}
# ---------------------------------------------------------------------------

@router.get("/{user_id}")
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Return a specific user's profile by ID.
    """

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {
        "id": user.id,
        "username": user.username,
        "is_active": user.is_active,
    }
