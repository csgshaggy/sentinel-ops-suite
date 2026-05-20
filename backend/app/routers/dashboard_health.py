# File: app/routers/dashboard_health.py
# Dashboard-facing IDRIM summary + run endpoints

from fastapi import APIRouter, HTTPException
from app.tools.security.idrim import IDRIMService

router = APIRouter(
    prefix="/dashboard/idrim",
    tags=["Dashboard • IDRIM"],
)

service = IDRIMService()


@router.get("/summary", response_model=dict)
async def idrim_dashboard_summary():
    """
    Dashboard tile summary for IDRIM.
    """
    try:
        baseline_exists = service.baseline_exists()
        last = service.load_last_result()

        if last is None:
            return {
                "baseline_exists": baseline_exists,
                "has_last_run": False,
                "integrity_score": None,
                "drift": None,
                "timestamp": None,
            }

        result = last if isinstance(last, dict) else last.model_dump()

        return {
            "baseline_exists": baseline_exists,
            "has_last_run": True,
            "integrity_score": result.get("integrity_score"),
            "drift": result.get("drift"),
            "timestamp": result.get("timestamp"),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/run", response_model=dict)
async def idrim_dashboard_run(payload: dict):
    """
    Trigger a synchronous IDRIM run from the dashboard tile.
    """
    try:
        result = service.run_analysis(payload)
        return result if isinstance(result, dict) else result.model_dump()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
