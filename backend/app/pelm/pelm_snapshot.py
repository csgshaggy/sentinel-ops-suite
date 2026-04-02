"""
PELM Snapshot Manager
Responsible for:
- Loading the latest snapshot from disk
- Returning structured metadata for dashboard consumption
- Ensuring safe, crash‑proof behavior when snapshots are missing
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

# Correct relative import (replaces invalid `backend.pelm`)
from . import pelm_plugin


SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), "snapshots")
SNAPSHOT_EXTENSION = ".json"


def _list_snapshot_files() -> list[str]:
    """Return all snapshot files in the snapshot directory."""
    if not os.path.exists(SNAPSHOT_DIR):
        return []
    return [
        f for f in os.listdir(SNAPSHOT_DIR)
        if f.endswith(SNAPSHOT_EXTENSION)
    ]


def _load_snapshot_file(path: str) -> Optional[Dict[str, Any]]:
    """Load a snapshot JSON file safely."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None


def load_latest_snapshot() -> Optional[Dict[str, Any]]:
    """
    Load the most recent snapshot based on filename timestamp.
    Returns a JSON‑safe dict or None if no snapshots exist.
    """

    files = _list_snapshot_files()
    if not files:
        return None

    # Sort by filename timestamp (assuming YYYYMMDD-HHMMSS.json)
    files.sort(reverse=True)
    latest = files[0]

    full_path = os.path.join(SNAPSHOT_DIR, latest)
    data = _load_snapshot_file(full_path)

    if data is None:
        return None

    # Add metadata for dashboard
    return {
        "snapshot_id": latest.replace(SNAPSHOT_EXTENSION, ""),
        "timestamp": data.get("timestamp"),
        "created_at": data.get("created_at"),
        "summary": data.get("summary", {}),
        "raw": data,
    }


def save_snapshot(snapshot: Dict[str, Any]) -> str:
    """
    Save a snapshot to disk using timestamp‑based filenames.
    Returns the snapshot filename.
    """

    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)

    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    filename = f"{ts}{SNAPSHOT_EXTENSION}"
    full_path = os.path.join(SNAPSHOT_DIR, filename)

    snapshot["timestamp"] = datetime.utcnow().isoformat() + "Z"

    with open(full_path, "w") as f:
        json.dump(snapshot, f, indent=2)

    return filename


def generate_snapshot() -> Dict[str, Any]:
    """
    Generate a new snapshot using the PELM plugin.
    This wraps the plugin output into a consistent structure.
    """

    raw = pelm_plugin.collect_snapshot()

    return {
        "created_at": datetime.utcnow().isoformat() + "Z",
        "summary": raw.get("summary", {}),
        "details": raw,
    }
