# SentinelOps — Unified Users Router (DB-backed sessions + RBAC)

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Cookie,
    UploadFile,
    File,
)
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import get_db
from app.core.sessions import get_session_by_id
from app.models.user import User
from app.schemas.user import UserOut

# Avatar services (local or S3 switchable)
from app.services.avatar_service import save_user_avatar, get_user_avatar_urls


# ------------------------------------------------------------
# Router definition — prefix REMOVED to avoid double-prefix drift
# Final paths become:
#   /api/users/me
#   /api/users/me/avatar
#   /api/users/
#   /api/users/{user_id}
# ------------------------------------------------------------
router = APIRouter(tags=["users"])


# ------------------------------------------------------------
# Internal helper — resolve authenticated user
# ------------------------------------------------------------
def get_authenticated_user(
    session_id: str | None,
    db: Session
) -> User:
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    # Normalize expires_at to timezone-aware UTC
    expires = session.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)

    if expires <= now:
        raise HTTPException(status_code=401, detail="Session expired")

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ------------------------------------------------------------
# Internal helper — admin check
# ------------------------------------------------------------
def require_admin(user: User):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")


# ------------------------------------------------------------
# GET /api/users/me — unified authenticated user endpoint
# ------------------------------------------------------------
@router.get("/me", response_model=UserOut)
async def get_me(
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user = get_authenticated_user(session_id, db)

    # Normalize avatar URLs (local or S3)
    avatar_url, avatar_thumb_url = get_user_avatar_urls(user)

    # Mutate ORM object so Pydantic returns correct fields
    user.avatar_url = avatar_url
    user.avatar_thumb_url = avatar_thumb_url

    return user


# ------------------------------------------------------------
# POST /api/users/me/avatar — upload avatar
# ------------------------------------------------------------
@router.post("/me/avatar")
async def upload_avatar(
    avatar: UploadFile = File(...),
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user = get_authenticated_user(session_id, db)

    if not avatar.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image uploads are allowed."
        )

    avatar_url = await save_user_avatar(db=db, user=user, file=avatar)

    return {"avatar_url": avatar_url}


# ------------------------------------------------------------
# GET /api/users — list all users (admin only)
# ------------------------------------------------------------
@router.get("/", response_model=list[UserOut])
async def list_users(
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user = get_authenticated_user(session_id, db)
    require_admin(user)

    users = db.query(User).all()
    return users


# ------------------------------------------------------------
# GET /api/users/{user_id} — admin only
# ------------------------------------------------------------
@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(
    user_id: int,
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user = get_authenticated_user(session_id, db)
    require_admin(user)

    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    return target
