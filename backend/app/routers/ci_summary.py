from fastapi import APIRouter
from pathlib import Path
import json
from datetime import datetime

router = APIRouter(prefix="/api/ci", tags=["ci"])

ROOT = Path(__file__).resolve().parents[3]
SUMMARY_FILE = ROOT / "artifacts" / "ci_summary.json"


@router.get("/summary")
def ci_summary():
    if not SUMMARY_FILE.exists():
        return {
            "backend": "fail",
            "frontend": "fail",
            "doctor": "fail",
            "makefile": "missing",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    try:
        data = json.loads(SUMMARY_FILE.read_text())
    except json.JSONDecodeError:
        return {
            "backend": "fail",
            "frontend": "fail",
            "doctor": "fail",
            "makefile": "missing",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    return {
        "backend": data.get("backend", "fail"),
        "frontend": data.get("frontend", "fail"),
        "doctor": data.get("doctor", "fail"),
        "makefile": data.get("makefile", "missing"),
        "timestamp": data.get("timestamp", datetime.utcnow().isoformat() + "Z"),
    }
