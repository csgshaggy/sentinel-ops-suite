"""
PELM Drift / Diff Engine
Computes drift summaries between snapshots or between
current state and canonical baselines.

This implementation is intentionally lightweight and safe:
- Never crashes the status endpoint
- Returns dashboard‑ready JSON
- Uses placeholder logic until real diffing is implemented
"""

from datetime import datetime
from typing import Dict, Any, Optional


def compute_drift_summary(
    baseline: Optional[Dict[str, Any]] = None,
    current: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Compute a drift summary between two states.
    If no data is provided, returns a neutral 'no drift' result.

    This placeholder implementation can be replaced with real diff logic.
    """

    # No data → no drift
    if baseline is None or current is None:
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "severity": "none",
            "summary": "No drift detected (no baseline or current state provided).",
            "details": {}
        }

    # Placeholder diff logic
    drift_detected = baseline != current

    if not drift_detected:
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "severity": "none",
            "summary": "No drift detected.",
            "details": {}
        }

    # If drift exists, return a simple structured summary
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "severity": "medium",
        "summary": "Drift detected between baseline and current state.",
        "details": {
            "baseline_keys": list(baseline.keys()),
            "current_keys": list(current.keys()),
            "note": "Placeholder diff engine — replace with real comparison logic."
        }
    }
