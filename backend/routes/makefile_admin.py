from __future__ import annotations

from fastapi import APIRouter

from backend.app.core.makefile_drift_detector import detect_drift

router = APIRouter(prefix="/makefile", tags=["makefile-admin"])


@router.get("/diff")
def diff() -> dict:
    """
    Return the Makefile drift report.
    """
    return detect_drift()
