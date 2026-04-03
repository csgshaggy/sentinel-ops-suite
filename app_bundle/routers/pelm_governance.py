from fastapi import APIRouter

from backend.pelm.pelm_tools import (
    detect_pelm_drift,
    repair_pelm,
    detect_pelm_regression,
)

router = APIRouter(prefix="/pelm/governance", tags=["PELM"])


@router.get("/drift")
def pelm_drift():
    return detect_pelm_drift()


@router.post("/repair")
def pelm_repair():
    return repair_pelm()


@router.get("/regression")
def pelm_regression():
    return detect_pelm_regression()
