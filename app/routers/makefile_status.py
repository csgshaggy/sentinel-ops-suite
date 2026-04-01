from fastapi import APIRouter
from backend.ci.makefile_tools import get_status, auto_repair, detect_drift

router = APIRouter(prefix="/makefile", tags=["Makefile"])

@router.get("/status")
def makefile_status():
    return get_status()

@router.get("/diff")
def makefile_diff():
    return detect_drift()

@router.post("/repair")
def makefile_repair():
    return auto_repair()
