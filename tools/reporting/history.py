"""
SuperDoctor Observability History Logger
Location: tools/reporting/history.py

Maintains an append‑only JSONL history file:
    reports/history.jsonl

Each entry contains:
- timestamp
- summary (health score, counts, mode)
- results (optional, depending on future config)
- git metadata (if available)
- project root reference

Cross‑platform (Windows + Linux).
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from utils.paths import ensure_directory

HISTORY_FILENAME = "history.jsonl"


def append_history_entry(project_root: Path, payload: Dict[str, Any]) -> Path:
    """
    Append a single JSONL entry to reports/history.jsonl.

    JSONL format = one JSON object per line.
    This is ideal for:
    - CI trend analysis
    - GitHub Pages dashboards
    - Local operator console history
    - Long‑term observability

    The file grows indefinitely by design.
    """
    reports_dir = project_root / "reports"
    ensure_directory(reports_dir)

    history_path = reports_dir / HISTORY_FILENAME

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "summary": payload.get("summary", {}),
        "git_sha": payload.get("summary", {}).get("git_sha"),
        "branch": payload.get("summary", {}).get("branch"),
        "health_score": payload.get("summary", {}).get("health_score"),
    }

    # Append as a single line
    with history_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    return history_path
