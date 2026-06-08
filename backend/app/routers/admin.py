# /app/routers/admin.py
# SentinelOps — Unified Admin Router (DB-backed sessions + RBAC)

from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.sessions import get_session_by_id
from app.models.user import User

router = APIRouter(prefix="/api/admin", tags=["admin"])


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
    if not session or session.expires_at <= session.expires_at.utcnow():
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
# GET /api/admin/dashboard — Admin Dashboard
# ------------------------------------------------------------
@router.get("/dashboard")
async def admin_dashboard(
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user = get_authenticated_user(session_id, db)
    require_admin(user)

    return {
        "message": "Welcome to the Admin Dashboard",
        "user": user.username,
        "role": user.role,
    }


# ------------------------------------------------------------
# GET /api/admin/audit-logs — Placeholder
# ------------------------------------------------------------
@router.get("/audit-logs")
async def audit_logs_disabled(
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    user = get_authenticated_user(session_id, db)
    require_admin(user)

    return {
        "detail": "Audit logging is not yet implemented. This endpoint is currently disabled."
    }
