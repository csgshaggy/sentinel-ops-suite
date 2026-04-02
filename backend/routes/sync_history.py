from fastapi import APIRouter
import os
import json
from pathlib import Path

router = APIRouter()

SNAPSHOT_DIR = Path(__file__).resolve().parents[2] / "repo-health-snapshots"


@router.get("/api/repo/sync-history")
def get_sync_history():
    """
    Returns a list of repo health snapshots created by the sync pipeline.
    Sorted newest → oldest.
    """

    if not SNAPSHOT_DIR.exists():
        return {"entries": []}

    entries = []

    for file in SNAPSHOT_DIR.glob("repo-health-*.json"):
        try:
            data = json.loads(file.read_text())
            timestamp = file.stem.replace("repo-health-", "")
            score = data.get("score", None)
            detail = data

            entries.append({
                "timestamp": timestamp,
                "score": score,
                "detail": detail,
            })
        except Exception:
            # Never break the dashboard
            continue

    # Sort newest → oldest
    entries.sort(key=lambda e: e["timestamp"], reverse=True)

    return {"entries": entries}
