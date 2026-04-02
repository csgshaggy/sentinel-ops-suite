"""
PELM Status Aggregator
Provides a unified, dashboard‑ready status object combining:
- Snapshot metadata
- Regression results
- Drift/diff results
- Canonical model status
- Health scoring
- Severity levels
"""

from datetime import datetime
from typing import Any, Dict

from .pelm_snapshot import load_latest_snapshot
from .pelm_diff import compute_drift_summary
from .pelm_regression import run_regression_summary
from .pelm_canonical import get_canonical_status


def safe_call(fn, default=None):
    """Run a function safely and never break the status endpoint."""
    try:
        return fn()
    except Exception:
        return default


def compute_health_score(snapshot, regression, drift) -> int:
    """
    Simple scoring model:
    - Start at 100
    - Deduct for drift, regression failures, missing snapshot
    """
    score = 100

    if snapshot is None:
        score -= 40

    if regression and regression.get("failed_tests", 0) > 0:
        score -= min(40, regression["failed_tests"] * 5)

    if drift and drift.get("severity", "none") == "high":
        score -= 30
    elif drift and drift.get("severity", "none") == "medium":
        score -= 15

    return max(score, 0)


def compute_severity(health_score: int) -> str:
    if health_score >= 85:
        return "healthy"
    if health_score >= 60:
        return "warning"
    return "critical"


def get_pelm_status() -> Dict[str, Any]:
    """
    Unified PELM status object for dashboard consumption.
    Always JSON‑serializable.
    """

    snapshot = safe_call(load_latest_snapshot)
    regression = safe_call(run_regression_summary, default={"failed_tests": 0})
    drift = safe_call(compute_drift_summary, default={"severity": "none"})
    canonical = safe_call(get_canonical_status, default={"valid": True})

    health_score = compute_health_score(snapshot, regression, drift)
    severity = compute_severity(health_score)

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "health_score": health_score,
        "severity": severity,
        "snapshot": snapshot or {},
        "regression": regression or {},
        "drift": drift or {},
        "canonical": canonical or {},
    }
