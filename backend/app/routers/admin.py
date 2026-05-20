# /home/ubuntu/sentinel-ops-suite/backend/app/routers/admin.py
# SentinelOps — Admin Router (Sync SQLAlchemy, RBAC, Audit Logs)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.models import AuditLog
from app.dependencies.auth import get_db, require_roles
from app.schemas.audit import AuditLogRead

router = APIRouter(prefix="/admin", tags=["Admin"])


# ---------------------------------------------------------
# List All Audit Logs (Admin Only)
# ---------------------------------------------------------
@router.get("/audit-logs", response_model=list[AuditLogRead])
def list_audit_logs(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),
):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
    return logs
