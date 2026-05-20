# app/routers/idrim_router.py

from __future__ import annotations
from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Dict, Any

    IDRIMService,
    IDRIMTasks,
    IDRIMSnapshot,
    IDRIMAnalysisResult,
    IDRIMDriftEvent,
    IDRIMBaseline,
)

# ---------------------------------------------------------
# Router Setup
# ---------------------------------------------------------
router = APIRouter(
    prefix="/idrim",
    tags=["IDRIM"],
)

# ---------------------------------------------------------
# Dependency: Construct Service + Tasks
# ---------------------------------------------------------
def get_idrim_service() -> IDRIMService:
    # Storage directory for baseline.json
    return IDRIMService(storage_path="data/idrim")

def get_idrim_tasks(
    service: IDRIMService = Depends(get_idrim_service)
) -> IDRIMTasks:
    return IDRIMTasks(service)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
@router.get("/health")
async def idrim_health():
    return {"status": "ok", "module": "IDRIM"}


# ---------------------------------------------------------
# Baseline Rebuild
# ---------------------------------------------------------
@router.post("/baseline/rebuild", response_model=IDRIMBaseline)
async def rebuild_baseline(
    snapshot: Dict[str, Any],
    service: IDRIMService = Depends(get_idrim_service),
):
    """
    Rebuild the IAM baseline from a snapshot.
    """
    baseline = service.rebuild_baseline(snapshot)
    return baseline


# ---------------------------------------------------------
# Drift Detection Only
# ---------------------------------------------------------
@router.post("/drift", response_model=list[IDRIMDriftEvent])
async def detect_drift(
    snapshot: Dict[str, Any],
    service: IDRIMService = Depends(get_idrim_service),
):
    """
    Return drift events without computing score.
    """
    events = service.detect_drift(snapshot)
    return events


# ---------------------------------------------------------
# Full Analysis
# ---------------------------------------------------------
@router.post("/analysis", response_model=IDRIMAnalysisResult)
async def run_analysis(
    snapshot: Dict[str, Any],
    service: IDRIMService = Depends(get_idrim_service),
):
    """
    Run full IDRIM analysis:
      • drift detection
      • scoring
      • structured result
    """
    result = service.run_analysis(snapshot)
    return result


# ---------------------------------------------------------
# Background Task: Full Analysis
# ---------------------------------------------------------
@router.post("/analysis/background")
async def run_analysis_background(
    snapshot: Dict[str, Any],
    background: BackgroundTasks,
    tasks: IDRIMTasks = Depends(get_idrim_tasks),
):
    """
    Run full analysis asynchronously.
    """
    background.add_task(tasks.analysis_task, snapshot)
    return {"status": "queued", "task": "analysis"}
