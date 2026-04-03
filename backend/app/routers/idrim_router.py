# backend/app/routers/idrim_router.py

from fastapi import APIRouter, HTTPException
from tools.security.idrim.idrim_engine import IDRIMEngine
from tools.security.idrim.idrim_models import IDRIMRequest, IDRIMResult
from tools.security.idrim.idrim_exceptions import IDRIMError

router = APIRouter(prefix="/idrim", tags=["IDRIM"])

# Instantiate engine once per router
engine = IDRIMEngine()


@router.post("/analyze", response_model=IDRIMResult)
def analyze_idrim(request: IDRIMRequest):
    """
    Run the IDRIM engine against an incoming request payload.
    """
    try:
        result = engine.analyze(request)
        return result
    except IDRIMError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/version")
def idrim_version():
    """
    Return the current IDRIM engine version.
    """
    return {"version": engine.version}


@router.get("/health")
def idrim_health():
    """
    Basic health check for the IDRIM subsystem.
    """
    return {"status": "ok", "engine": "IDRIM", "version": engine.version}
