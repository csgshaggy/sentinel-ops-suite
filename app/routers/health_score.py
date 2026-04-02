from fastapi import APIRouter
from backend.health.health_score import compute_health_score

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/score")
def get_health_score():
    return compute_health_score()
