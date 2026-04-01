import json
from typing import Any, Dict


def _safe_get(d: Dict[str, Any], key: str, default=None):
    return d.get(key, default) if isinstance(d, dict) else default


def diff_snapshots(left: Dict[str, Any], right: Dict[str, Any]) -> Dict[str, Any]:
    """
    Produce a structured diff between two PELM snapshots.
    Focuses on:
      - risk
      - status
      - signals
      - metadata
    """

    left_risk = _safe_get(left, "risk")
    right_risk = _safe_get(right, "risk")

    left_status = _safe_get(left, "status")
    right_status = _safe_get(right, "status")

    left_signals = _safe_get(left, "signals", {})
    right_signals = _safe_get(right, "signals", {})

    left_meta = _safe_get(left, "metadata", {})
    right_meta = _safe_get(right, "metadata", {})

    return {
        "risk": {
            "left": left_risk,
            "right": right_risk,
            "changed": left_risk != right_risk,
        },
        "status": {
            "left": left_status,
            "right": right_status,
            "changed": left_status != right_status,
        },
        "signals": {
            "left": left_signals,
            "right": right_signals,
            "changed": left_signals != right_signals,
        },
        "metadata": {
            "left": left_meta,
            "right": right_meta,
            "changed": left_meta != right_meta,
        },
        "raw": {
            "left": left,
            "right": right,
        },
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: pelm_diff.py left.json right.json")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        left = json.load(f)
    with open(sys.argv[2]) as f:
        right = json.load(f)

    print(json.dumps(diff_snapshots(left, right), indent=2))
