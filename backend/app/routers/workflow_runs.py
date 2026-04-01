from fastapi import APIRouter, Query
from typing import Any, Dict
from pathlib import Path
import subprocess
import json
import sys

router = APIRouter(prefix="/workflow-runs", tags=["workflow-runs"])

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "scripts" / "workflow_runs.py"


@router.get("/", summary="Get recent GitHub workflow runs")
def get_workflow_runs(limit: int = Query(20, ge=1, le=100)) -> Dict[str, Any]:
    if not SCRIPT.exists():
        return {"runs": [], "error": "workflow_runs.py not found"}

    cmd = [sys.executable, str(SCRIPT), "--json", "--limit", str(limit)]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.returncode != 0:
        return {"runs": [], "error": proc.stderr.strip()}

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"runs": [], "error": "Invalid JSON output"}

    if isinstance(data, list):
        return {"runs": data}

    return {"runs": data.get("runs", [])}
