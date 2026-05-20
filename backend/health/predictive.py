import numpy as np
from backend.health.health_trend import load_trend

PREDICTION_WINDOWS = {
    "1h": 3600,
    "6h": 21600,
    "24h": 86400,
}

def compute_prediction():
    trend = load_trend()
    if len(trend) < 3:
        return {"error": "Not enough data for prediction"}

    timestamps = np.array([t["timestamp"] for t in trend])
    scores = np.array([t["score"] for t in trend])

    # Normalize timestamps for numerical stability
    t0 = timestamps[0]
    x = timestamps - t0
    y = scores

    # Linear regression
    slope, intercept = np.polyfit(x, y, 1)

    predictions = {}
    for label, offset in PREDICTION_WINDOWS.items():
        future_x = x[-1] + offset
        future_score = slope * future_x + intercept
        predictions[label] = round(float(future_score), 2)

    # Risk assessment
    risk = "low"
    if slope < -0.01:
        risk = "medium"
    if slope < -0.05:
        risk = "high"

    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "current_score": float(scores[-1]),
        "predictions": predictions,
        "risk": risk,
    }
