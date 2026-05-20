from fastapi import APIRouter
import subprocess
import json
from pathlib import Path

router = APIRouter()

def compute_health():
    """
    Replace this logic with your real health checks.
    This is a placeholder that checks:
    - venv exists
    - Makefile exists
    - Git repo is clean
    """

    project_root = Path.home() / "sentinel-ops-suite"
    backend_dir = project_root / "backend"
    venv_dir = backend_dir / ".venv"
    makefile = project_root / "Makefile"

    health = {
        "venv": venv_dir.exists(),
        "makefile": makefile.exists(),
        "git_clean": True,
    }

    # Git cleanliness check
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(project_root),
            capture_output=True,
            text=True
        )
        health["git_clean"] = (result.stdout.strip() == "")
    except Exception:
        health["git_clean"] = False

    # Compute final status
    if all(health.values()):
        return "OK"
    return "DEGRADED"

@router.get("/health")
def dashboard_health():
    status = compute_health()
    return {"status": status}
