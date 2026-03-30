from sqlalchemy.orm import Session
from backend.auth.models import AuditLog

def log_event(
    db: Session,
    *,
    actor_email: str | None,
    action: str,
    target: str | None = None,
    details: str | None = None,
):
    entry = AuditLog(
        actor_email=actor_email,
        action=action,
        target=target,
        details=details,
    )
    db.add(entry)
    db.commit()
