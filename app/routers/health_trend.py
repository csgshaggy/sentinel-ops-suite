from fastapi import APIRouter
from backend.health.health_trend import get_trend, append_score

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/trend")
def health_trend():
    return get_trend()

@router.post("/trend/update")
def update_trend():
    return append_score()
