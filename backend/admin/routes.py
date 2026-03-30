# =====================================================================
# SSRF Command Console — Admin API
# User CRUD • Password Reset • Audit Logs • Metrics Dashboard
# =====================================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import secrets

from backend.database import get_db
from backend.auth.models import User as UserModel, AuditLog
from backend.auth.security import hash_password
from backend.auth.dependencies import require_role, get_current_user
from backend.auth.audit import log_event
from backend.admin.schemas import (
    AdminUserOut,
    AdminUserCreate,
    AdminUserUpdate,
    AuditLogOut,
)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_role("admin"))],  # admin-only
)

# ---------------------------------------------------------------------
# List Users
# ---------------------------------------------------------------------
@router.get("/users", response_model=list[AdminUserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()

# ---------------------------------------------------------------------
# Create User
# ---------------------------------------------------------------------
@router.post("/users", response_model=AdminUserOut)
def create_user(
    payload: AdminUserCreate,
    db: Session = Depends(get_db),
    actor: UserModel = Depends(get_current_user),
):
    existing = db.query(UserModel).filter(UserModel.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = UserModel(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    log_event(
        db,
        actor_email=actor.email,
        action="user_create",
        target=f"user:{user.email}",
        details=f"Role={user.role}",
    )

    return user

# ---------------------------------------------------------------------
# Update User (role + active state)
# ---------------------------------------------------------------------
@router.put("/users/{user_id}", response_model=AdminUserOut)
def update_user(
    user_id: int,
    payload: AdminUserUpdate,
    db: Session = Depends(get_db),
    actor: UserModel = Depends(get_current_user),
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = payload.role
    user.is_active = payload.is_active

    db.commit()
    db.refresh(user)

    log_event(
        db,
        actor_email=actor.email,
        action="user_update",
        target=f"user:{user.email}",
        details=f"Role={user.role}, Active={user.is_active}",
    )

    return user

# ---------------------------------------------------------------------
# Reset Password (Admin-Initiated)
# ---------------------------------------------------------------------
@router.post("/users/{user_id}/reset-password")
def reset_password(
    user_id: int,
    db: Session = Depends(get_db),
    actor: UserModel = Depends(get_current_user),
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    temp_password = secrets.token_urlsafe(10)

    user.hashed_password = hash_password(temp_password)
    db.commit()

    log_event(
        db,
        actor_email=actor.email,
        action="password_reset",
        target=f"user:{user.email}",
        details="Admin-initiated password reset",
    )

    return {"temporary_password": temp_password}

# ---------------------------------------------------------------------
# Audit Logs
# ---------------------------------------------------------------------
@router.get("/audit-logs", response_model=list[AuditLogOut])
def list_audit_logs(db: Session = Depends(get_db)):
    return (
        db.query(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .limit(200)
        .all()
    )

# ---------------------------------------------------------------------
# Metrics Dashboard Endpoint
# ---------------------------------------------------------------------
@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    # Total users
    total_users = db.query(func.count(UserModel.id)).scalar()

    # Active vs inactive
    active_users = (
        db.query(func.count(UserModel.id))
        .filter(UserModel.is_active == True)
        .scalar()
    )
    inactive_users = total_users - active_users

    # Role distribution
    roles = (
        db.query(UserModel.role, func.count(UserModel.id))
        .group_by(UserModel.role)
        .all()
    )
    role_counts = {role: count for role, count in roles}

    # Recent login activity (last 7 days)
    recent_logins = (
        db.query(func.count(AuditLog.id))
        .filter(AuditLog.action == "login")
        .filter(
            AuditLog.timestamp >= func.now() - func.cast("7 days", db.bind.dialect.interval)
        )
        .scalar()
    )

    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "roles": role_counts,
        "recent_logins": recent_logins,
    }
