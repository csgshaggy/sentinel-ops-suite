from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
import json

from backend.pelm.pelm_diff import diff_snapshots

router = APIRouter(prefix="/pelm", tags=["PELM Diff"])

SNAPSHOT_DIR = Path("backend/pelm/snapshots")


@router.get("/snapshots/diff")
def pelm_snapshot_diff(
    left: str = Query(..., description="Left snapshot filename"),
    right: str = Query(..., description="Right snapshot filename"),
):
    """
    Compare two PELM snapshots and return a structured diff.
    """

    left_path = SNAPSHOT_DIR / left
    right_path = SNAPSHOT_DIR / right

    if not left_path.exists():
        raise HTTPException(status_code=404, detail=f"Left snapshot not found: {left}")

    if not right_path.exists():
        raise HTTPException(status_code=404, detail=f"Right snapshot not found: {right}")

    try:
        left_data = json.loads(left_path.read_text())
        right_data = json.loads(right_path.read_text())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading snapshots: {e}")

    diff = diff_snapshots(left_data, right_data)
    return diff
