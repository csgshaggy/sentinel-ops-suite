from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(prefix="/api/plugins", tags=["plugins"])

ROOT = Path(__file__).resolve().parents[3]
DRIFT_FILE = ROOT / "data" / "router_drift.json"


@router.get("/router-drift")
def router_drift():
    if not DRIFT_FILE.exists():
        return {
            "status": "ok",
            "missing": [],
            "extra": [],
            "ordered": True,
            "expected_order": [],
            "actual_order": [],
        }

    try:
        data = json.loads(DRIFT_FILE.read_text())
    except json.JSONDecodeError:
        return {
            "status": "degraded",
            "missing": [],
            "extra": [],
            "ordered": False,
            "expected_order": [],
            "actual_order": [],
        }

    return {
        "status": data.get("status", "ok"),
        "missing": data.get("missing", []),
        "extra": data.get("extra", []),
        "ordered": data.get("ordered", True),
        "expected_order": data.get("expected_order", []),
        "actual_order": data.get("actual_order", []),
    }
