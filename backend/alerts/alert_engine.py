from backend.health.health_trend import load_trend
from backend.anomaly.correlation import correlate_anomaly

def evaluate_alerts():
    trend = load_trend()
    if not trend:
        return []

    latest = trend[-1]
    alerts = []

    # ---------------------------------------------------------
    # Rule 1: Health score drop
    # ---------------------------------------------------------
    if latest["score"] < 60:
        alerts.append({
            "type": "health_score_low",
            "message": f"Health score dropped to {latest['score']}",
            "severity": "high",
        })

    # ---------------------------------------------------------
    # Rule 2: CPU saturation
    # ---------------------------------------------------------
    if latest["cpu"] > 85:
        alerts.append({
            "type": "cpu_high",
            "message": f"CPU at {latest['cpu']}%",
            "severity": "medium",
        })

    # ---------------------------------------------------------
    # Rule 3: Memory saturation
    # ---------------------------------------------------------
    if latest["memory"] > 85:
        alerts.append({
            "type": "memory_high",
            "message": f"Memory at {latest['memory']}%",
            "severity": "medium",
        })

    # ---------------------------------------------------------
    # Rule 4: Disk saturation
    # ---------------------------------------------------------
    if latest["disk"] > 90:
        alerts.append({
            "type": "disk_high",
            "message": f"Disk usage at {latest['disk']}%",
            "severity": "high",
        })

    return alerts


def correlate_alert_with_anomaly(anomaly_timestamp: int):
    """
    Combine anomaly correlation + alert rules.
    """
    correlation = correlate_anomaly(anomaly_timestamp)
    alerts = evaluate_alerts()

    return {
        "correlation": correlation,
        "active_alerts": alerts,
    }
