from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(prefix="/pelm", tags=["PELM Trend"])

SNAPSHOT_DIR = Path("backend/pelm/snapshots")


@router.get("/snapshots/trend")
def pelm_risk_trend():
    """
    Returns a list of:
      { "timestamp": "...", "risk": "low|medium|high" }
    extracted from all PELM snapshots.
    """

    trend = []

    for snap_path in sorted(SNAPSHOT_DIR.glob("pelm-*.json")):
        try:
            snap = json.loads(snap_path.read_text())
            ts = snap.get("metadata", {}).get("timestamp")
            risk = snap.get("risk")

            if ts and risk:
                trend.append({"timestamp": ts, "risk": risk})
        except Exception:
            continue

    return {"trend": trend}
