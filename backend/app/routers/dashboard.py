# backend/app/routers/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.users import get_current_user
from app import models

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


# ---------------------------------------------------------------------------
# DASHBOARD SUMMARY ENDPOINT
# ---------------------------------------------------------------------------

@router.get("/summary")
async def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Return dashboard tiles, alerts, and system health.
    Placeholder values for now — real metrics will be wired in Item 3.
    """

    # Placeholder system health
    system_health = {
        "cpu_load": "nominal",
        "memory_usage": "stable",
        "disk_status": "ok",
    }

    # Placeholder alerts
    alerts = [
        {"id": 1, "severity": "low", "message": "No recent anomalies detected."},
    ]

    # Placeholder tiles
    tiles = [
        {"name": "Active Sessions", "value": 3},
        {"name": "Open Incidents", "value": 0},
        {"name": "Last Scan", "value": "OK"},
    ]

    return {
        "status": "ok",
        "user": {
            "id": current_user.id,
            "username": current_user.username,
        },
        "system_health": system_health,
        "alerts": alerts,
        "tiles": tiles,
    }
