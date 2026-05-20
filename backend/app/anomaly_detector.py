import json
from pathlib import Path
from typing import Any, Dict, List

from .adaptive_thresholds import compute_adaptive_thresholds, load_thresholds
from .predictive_model import predict_health

HISTORY_FILE = Path("health_history.jsonl")
ANOMALY_FILE = Path("anomalies.jsonl")


def _load_recent_history(window: int) -> List[Dict[str, Any]]:
    """Load the most recent N history entries."""
    if not HISTORY_FILE.exists():
        return []

    lines = HISTORY_FILE.read_text().strip().split("\n")[-window:]
    return [json.loads(line) for line in lines if line.strip()]


def detect_predictive_anomalies() -> List[Dict[str, Any]]:
    """
    Uses the predictive model to detect future‑oriented anomalies.
    """
    result = predict_health(5)
    future_scores = result.get("predictions", [])
    slope = result.get("trend_slope", 0.0)

    anomalies: List[Dict[str, Any]] = []

    if future_scores and any(score < 40 for score in future_scores):
        anomalies.append(
            {
                "type": "predicted_low_score",
                "message": "Predicted health score will fall below 40",
                "future_scores": future_scores,
            }
        )

    if slope < -5:
        anomalies.append(
            {
                "type": "negative_future_trend",
                "message": "Future trend slope is sharply negative",
                "slope": slope,
            }
        )

    return anomalies


def detect_anomalies(window: int = 10) -> List[Dict[str, Any]]:
    """
    Detects anomalies based on:
    - adaptive low score threshold
    - adaptive sudden drop threshold
    - adaptive negative trend slope
    - predictive anomalies (future‑oriented)
    """

    history = _load_recent_history(window)
    if not history:
        return []

    thresholds = load_thresholds()
    low_score_threshold = thresholds["low_score_threshold"]
    sudden_drop_threshold = thresholds["sudden_drop_threshold"]
    trend_slope_threshold = thresholds["trend_slope_threshold"]

    anomalies: List[Dict[str, Any]] = []

    # 1. Score below adaptive threshold
    for entry in history:
        if entry["score"] < low_score_threshold:
            anomalies.append(
                {
                    "type": "low_score",
                    "score": entry["score"],
                    "timestamp": entry["timestamp"],
                    "threshold": low_score_threshold,
                    "message": (
                        f"Health score dropped below adaptive threshold "
                        f"{low_score_threshold}"
                    ),
                }
            )

    # 2. Sudden drop detection (adaptive)
    for previous, current in zip(history, history[1:]):
        drop_amount = previous["score"] - current["score"]
        if drop_amount > sudden_drop_threshold:
            anomalies.append(
                {
                    "type": "sudden_drop",
                    "from": previous["score"],
                    "to": current["score"],
                    "delta": drop_amount,
                    "threshold": sudden_drop_threshold,
                    "timestamp": current["timestamp"],
                    "message": "Sudden health score drop detected (adaptive threshold)",
                }
            )

    # 3. Trend slope detection (simple start vs end, adaptive)
    scores = [entry["score"] for entry in history]
    if len(scores) >= 3:
        slope = scores[-1] - scores[0]
        if slope < trend_slope_threshold:
            anomalies.append(
                {
                    "type": "negative_trend",
                    "from": scores[0],
                    "to": scores[-1],
                    "slope": slope,
                    "threshold": trend_slope_threshold,
                    "message": "Negative health trend detected (adaptive threshold)",
                }
            )

    # 4. Predictive anomalies (future‑oriented)
    anomalies.extend(detect_predictive_anomalies())

    # Persist anomalies
    if anomalies:
        with ANOMALY_FILE.open("a", encoding="utf-8") as file:
            for anomaly in anomalies:
                file.write(json.dumps(anomaly) + "\n")

    # Recompute thresholds after each detection pass
    compute_adaptive_thresholds()

    return anomalies
