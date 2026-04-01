from fastapi import APIRouter
from backend.anomaly.correlation import correlate_anomaly

router = APIRouter(prefix="/anomaly", tags=["Anomalies"])

@router.get("/correlate")
def correlate(ts: int):
    """
    ts = anomaly timestamp (epoch seconds)
    """
    return correlate_anomaly(ts)
