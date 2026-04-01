from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from tools.plugins.pelm import get_pelm_metadata, run_pelm_scan

router = APIRouter(prefix="/pelm", tags=["PELM"])


@router.get("/summary")
def get_pelm_summary() -> Dict[str, Any]:
    """
    Returns the PELM summary block:
    - high-level status
    - last scan timestamp
    - risk score
    - metadata
    """
    try:
        result = run_pelm_scan()
        return {
            "status": result.get("status", "unknown"),
            "last_scan": result.get("timestamp"),
            "risk_score": result.get("risk_score"),
            "metadata": get_pelm_metadata(),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/events")
def get_pelm_events() -> List[Dict[str, Any]]:
    """
    Returns the last N PELM events (non-streaming).
    The streaming version is handled in pelm_stream.py.
    """
    try:
        result = run_pelm_scan()
        return result.get("events", [])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/risks")
def get_pelm_risks() -> List[Dict[str, Any]]:
    """
    Returns the PELM risk surface:
    - risk categories
    - severity
    - affected components
    """
    try:
        result = run_pelm_scan()
        return result.get("risks", [])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/graph")
def get_pelm_graph() -> Dict[str, Any]:
    """
    Returns the PELM dependency/relationship graph.
    """
    try:
        result = run_pelm_scan()
        return result.get("graph", {})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
