from fastapi import APIRouter
from app.pelm.pelm_status import get_pelm_status

router = APIRouter()

@router.get("/pelm/status")
def pelm_status():
    return get_pelm_status()
