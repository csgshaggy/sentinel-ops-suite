"""
PELM Utility Tools
Shared helpers used across the PELM subsystem.

This module provides:
- Safe JSON helpers
- Timestamp utilities
- Lightweight hashing
- Deep comparison helpers (placeholder)
"""

import json
import hashlib
from datetime import datetime
from typing import Any, Dict


def utc_now() -> str:
    """Return a UTC timestamp in ISO format."""
    return datetime.utcnow().isoformat() + "Z"


def safe_json_dumps(data: Any) -> str:
    """Safely convert Python objects to JSON."""
    try:
        return json.dumps(data, indent=2)
    except Exception:
        return "{}"


def compute_hash(data: Any) -> str:
    """
    Compute a stable hash for any JSON‑serializable object.
    Useful for canonical integrity checks.
    """
    try:
        encoded = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()
    except Exception:
        return "invalid-hash"


def deep_compare(a: Any, b: Any) -> Dict[str, Any]:
    """
    Placeholder deep comparison tool.
    Returns a structured diff summary.
    """
    if a == b:
        return {
            "equal": True,
            "differences": [],
            "summary": "Objects are identical."
        }

    return {
        "equal": False,
        "differences": ["placeholder-diff"],
        "summary": "Objects differ (placeholder diff engine)."
    }
