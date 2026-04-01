from backend.health.health_score import compute_health_score
from backend.health.health_trend import load_trend
from backend.health.predictive import compute_prediction
from backend.alerts.alert_engine import evaluate_alerts
from backend.anomaly.correlation import correlate_anomaly
from backend.ci.makefile_tools import get_status as makefile_status

def build_observability_summary():
    trend = load_trend()
    latest_anomaly = trend[-1]["timestamp"] if trend else None

    return {
        "health": compute_health_score(),
        "trend": trend[-20:],  # last 20 points
        "prediction": compute_prediction(),
        "alerts": evaluate_alerts(),
        "makefile": makefile_status(),
        "latest_anomaly_correlation": (
            correlate_anomaly(latest_anomaly) if latest_anomaly else None
        ),
    }
