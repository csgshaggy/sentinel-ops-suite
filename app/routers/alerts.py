from fastapi import APIRouter
from backend.alerts.alert_engine import evaluate_alerts, correlate_alert_with_anomaly

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/")
def get_alerts():
    return evaluate_alerts()

@router.get("/correlate")
def correlate(ts: int):
    return correlate_alert_with_anomaly(ts)
