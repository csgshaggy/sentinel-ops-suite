from fastapi import APIRouter
from pathlib import Path
import difflib
import subprocess
import sys

router = APIRouter(prefix="/api/makefile", tags=["makefile"])

ROOT = Path(__file__).resolve().parents[3]
MAKEFILE = ROOT / "Makefile"
SNAPSHOT = ROOT / "data" / "Makefile.snapshot"
REPAIR_ENGINE = ROOT / "backend" / "app" / "repair_engine.py"


@router.get("/health")
def makefile_health():
    if not MAKEFILE.exists() or not SNAPSHOT.exists():
        return {
            "status": "missing",
            "adds": 0,
            "removes": 0,
            "message": "Makefile or snapshot missing",
        }

    current = MAKEFILE.read_text().splitlines()
    baseline = SNAPSHOT.read_text().splitlines()

    diff = difflib.ndiff(baseline, current)
    adds = 0
    removes = 0
    for d in diff:
        if d.startswith("+ "):
            adds += 1
        elif d.startswith("- "):
            removes += 1

    if adds == 0 and removes == 0:
        status = "ok"
        message = "Makefile in sync with snapshot"
    else:
        status = "drift"
        message = "Makefile drift detected vs snapshot"

    return {
        "status": status,
        "adds": adds,
        "removes": removes,
        "message": message,
    }


@router.post("/heal")
def makefile_heal():
    if not REPAIR_ENGINE.exists():
        return {"ok": False, "message": "repair_engine.py not found"}

    cmd = [sys.executable, str(REPAIR_ENGINE), "--mode", "makefile-heal"]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.returncode != 0:
        return {
            "ok": False,
            "message": proc.stderr.strip() or "Makefile heal failed",
        }

    return {
        "ok": True,
        "message": proc.stdout.strip() or "Makefile restored from snapshot",
    }
