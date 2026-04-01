from fastapi import APIRouter
from pathlib import Path
import difflib
import subprocess
import sys
import json

router = APIRouter(prefix="/api/repo", tags=["repo"])

ROOT = Path(__file__).resolve().parents[3]
MAKEFILE = ROOT / "Makefile"
MAKEFILE_SNAPSHOT = ROOT / "data" / "Makefile.snapshot"
ROUTER_DRIFT_FILE = ROOT / "data" / "router_drift.json"
HEALTH_SCORE_SCRIPT = ROOT / "backend" / "health" / "run_daily_score.py"


def _makefile_status() -> str:
    if not MAKEFILE.exists() or not MAKEFILE_SNAPSHOT.exists():
        return "missing"
    current = MAKEFILE.read_text().splitlines()
    baseline = MAKEFILE_SNAPSHOT.read_text().splitlines()
    diff = list(difflib.unified_diff(baseline, current))
    return "ok" if not diff else "drift"


def _router_status() -> str:
    if not ROUTER_DRIFT_FILE.exists():
        return "ok"
    try:
        data = json.loads(ROUTER_DRIFT_FILE.read_text())
    except json.JSONDecodeError:
        return "drift"
    return "ok" if data.get("status") == "ok" else "drift"


def _git_status() -> str:
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            return "drift"
        return "ok" if not proc.stdout.strip() else "drift"
    except Exception:
        return "drift"


def _system_status() -> str:
    if not HEALTH_SCORE_SCRIPT.exists():
        return "warn"
    try:
        proc = subprocess.run(
            [sys.executable, str(HEALTH_SCORE_SCRIPT)],
            cwd=ROOT / "backend",
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            return "fail"
        return "ok"
    except Exception:
        return "fail"


@router.get("/health")
def repo_health():
    makefile = _makefile_status()
    router = _router_status()
    git = _git_status()
    system = _system_status()

    score = 100
    if makefile != "ok":
        score -= 20
    if router != "ok":
        score -= 20
    if git != "ok":
        score -= 20
    if system == "warn":
        score -= 10
    elif system == "fail":
        score -= 30

    score = max(0, min(100, score))

    return {
        "makefile": makefile if makefile != "ok" else "ok",
        "router": router if router != "ok" else "ok",
        "git": git if git != "ok" else "ok",
        "system": system,
        "score": score,
    }
