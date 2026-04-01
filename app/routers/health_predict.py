from fastapi import APIRouter
from backend.health.predictive import compute_prediction

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/predict")
def predict():
    return compute_prediction()
