from fastapi import APIRouter, HTTPException
    IDRIMService,
    IDRIMTaskRunner,
    IDRIMRequest,
    IDRIMResult,
)

router = APIRouter(prefix="/idrim", tags=["IDRIM API"])

service = IDRIMService()
tasks = IDRIMTaskRunner()


@router.get("/health")
async def idrim_health():
    """
    Basic health check for the IDRIM subsystem.
    """
    try:
        return {
            "status": "ok",
            "baseline_exists": service.baseline_exists(),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/analyze", response_model=IDRIMResult)
async def idrim_analyze(request: IDRIMRequest):
    """
    Run a synchronous IDRIM analysis.
    """
    try:
        return service.run_analysis(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/baseline")
async def idrim_set_baseline(request: IDRIMRequest):
    """
    Save a new baseline snapshot.
    """
    try:
        service.save_baseline(request.payload)
        return {"status": "baseline_saved"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/baseline")
async def idrim_get_baseline():
    """
    Retrieve the stored baseline snapshot.
    """
    try:
        baseline = service.load_baseline()
        if baseline is None:
            raise HTTPException(status_code=404, detail="No baseline found")
        return baseline
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/task", response_model=dict)
async def idrim_start_task(request: IDRIMRequest):
    """
    Start a long-running IDRIM task (daily scan, batch job, etc.).
    Returns a task_id for SSE streaming.
    """
    try:
        task_id = tasks.start_task(request)
        return {"task_id": task_id}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/task/{task_id}", response_model=dict)
async def idrim_task_status(task_id: str):
    """
    Query the status of a running or completed task.
    """
    try:
        status = tasks.get_status(task_id)
        if status is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return status
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
