from fastapi import APIRouter
from backend.observability.summary import build_observability_summary

router = APIRouter(prefix="/observability", tags=["Observability"])


@router.get("/summary")
def summary():
    return build_observability_summary()
