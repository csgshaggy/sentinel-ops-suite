import math
from backend.health.health_trend import load_trend

def correlate_anomaly(anomaly_timestamp: int):
    trend = load_trend()
    if not trend:
        return {"error": "No trend data available"}

    # Find nearest health score entry
    nearest = min(
        trend,
        key=lambda t: abs(t["timestamp"] - anomaly_timestamp)
    )

    delta_t = abs(nearest["timestamp"] - anomaly_timestamp)

    correlation = {
        "anomaly_timestamp": anomaly_timestamp,
        "nearest_health_timestamp": nearest["timestamp"],
        "time_offset_seconds": delta_t,
        "health_score": nearest["score"],
        "cpu": nearest["cpu"],
        "memory": nearest["memory"],
        "disk": nearest["disk"],
        "severity_hint": compute_severity_hint(nearest),
    }

    return correlation


def compute_severity_hint(entry):
    score = entry["score"]
    cpu = entry["cpu"]
    mem = entry["memory"]
    disk = entry["disk"]

    hints = []

    if score < 60:
        hints.append("Low health score")

    if cpu > 80:
        hints.append("High CPU load")

    if mem > 80:
        hints.append("High memory usage")

    if disk > 85:
        hints.append("Disk saturation")

    return hints or ["No significant health degradation"]
