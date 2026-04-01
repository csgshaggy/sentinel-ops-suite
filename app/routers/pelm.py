from fastapi import APIRouter

router = APIRouter(prefix="/pelm", tags=["pelm"])

@router.get("/health")
async def pelm_health():
    return {"status": "ok", "module": "pelm"}
