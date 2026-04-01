# backend/app/routers/idrim_router.py

from fastapi import APIRouter
from tools.security.idrim.idrim_engine import IDRIMEngine

router = APIRouter(prefix="/idrim", tags=["IDRIM"])

# Instantiate engine once per router
engine = IDRIMEngine()


@router.get("/run")
def run_idrim():
    """
    Executes the full IDRIM engine:
    - Collect IAM state
    - Load baseline
    - Analyze drift
    - Emit events
    Returns drift events.
    """
    events = engine.run()
    return {"events": events}


@router.post("/baseline/rebuild")
def rebuild_baseline():
    """
    Rebuilds the IAM baseline snapshot.
    Returns the new baseline.
    """
    baseline = engine.rebuild_baseline()
    return {"baseline": baseline}


@router.get("/diff")
def idrim_diff():
    """
    Returns a structured diff between baseline and current IAM state.
    Does NOT emit events.
    """
    diff = engine.diff()
    return {"diff": diff}


@router.get("/events")
def idrim_events_placeholder():
    """
    Placeholder for SSE event streaming.
    """
    return {"status": "SSE endpoint not yet implemented"}
