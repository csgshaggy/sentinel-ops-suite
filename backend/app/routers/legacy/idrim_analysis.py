# app/routers/idrim_analysis.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from tools.security.idrim.idrim_service import IDRIMService
from tools.security.idrim.idrim_tasks import IDRIMTaskRunner
from tools.security.idrim.idrim_models import IDRIMRequest, IDRIMResult

router = APIRouter(prefix="/idrim", tags=["IDRIM"])

# Instantiate service + task runner
service = IDRIMService()
tasks = IDRIMTaskRunner()


@router.get("/health")
async def idrim_health():
    """
    Lightweight health check for the IDRIM subsystem.
    Confirms the service is reachable and whether a baseline exists.
    """
    try:
        baseline_exists = service.baseline_exists()
        return {"status": "ok", "baseline_exists": baseline_exists}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/run", response_model=IDRIMResult)
async def idrim_run(request: IDRIMRequest):
    """
    Run a full IDRIM analysis against the provided snapshot payload.
    This is synchronous for now; SSE handles streaming output separately.
    """
    try:
        result = service.run(request)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/tasks/run")
async def idrim_run_task(request: IDRIMRequest):
    """
    Run the IDRIM task runner (async job orchestration).
    Useful for long‑running or scheduled analysis flows.
    """
    try:
        task_id = tasks.enqueue(request)
        return {"status": "queued", "task_id": task_id}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
