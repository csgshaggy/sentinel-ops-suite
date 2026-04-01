import json
from pathlib import Path
from typing import Dict, List, Any

SNAPSHOT_DIR = Path("backend/pelm/snapshots")


def load_all_snapshots() -> List[Dict[str, Any]]:
    """Load all PELM snapshots sorted by timestamp."""
    snapshots = []

    for snap_path in sorted(SNAPSHOT_DIR.glob("pelm-*.json")):
        try:
            snap = json.loads(snap_path.read_text())
            snapshots.append(snap)
        except Exception:
            continue

    return snapshots


def risk_to_value(risk: str) -> int:
    if risk == "low":
        return 1
    if risk == "medium":
        return 2
    if risk == "high":
        return 3
    return 0


def compute_regression_score(snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes regression analytics across all snapshots.

    Outputs:
      - risk_trend: list of numeric risk values
      - risk_delta: last - first
      - risk_acceleration: slope of last 3 points
      - drift_detected: boolean
      - regression_score: 0–100
    """

    if len(snapshots) < 2:
        return {
            "risk_trend": [],
            "risk_delta": 0,
            "risk_acceleration": 0,
            "drift_detected": False,
            "regression_score": 0,
        }

    # Convert risk to numeric values
    values = [risk_to_value(s.get("risk")) for s in snapshots]

    # Risk delta (overall change)
    risk_delta = values[-1] - values[0]

    # Risk acceleration (slope of last 3 points)
    if len(values) >= 3:
        v1, v2, v3 = values[-3:]
        risk_acceleration = (v3 - v2) + (v2 - v1)
    else:
        risk_acceleration = values[-1] - values[-2]

    # Drift detection: any signal-level changes across snapshots
    drift_detected = False
    for i in range(len(snapshots) - 1):
        if snapshots[i].get("signals") != snapshots[i + 1].get("signals"):
            drift_detected = True
            break

    # Regression score (0–100)
    # Higher = worse
    score = 0
    score += max(0, risk_delta * 10)
    score += max(0, risk_acceleration * 15)
    if drift_detected:
        score += 25

    score = min(score, 100)

    return {
        "risk_trend": values,
        "risk_delta": risk_delta,
        "risk_acceleration": risk_acceleration,
        "drift_detected": drift_detected,
        "regression_score": score,
    }


def analyze_regression() -> Dict[str, Any]:
    """Main entry point for regression analytics."""
    snapshots = load_all_snapshots()
    return compute_regression_score(snapshots)
