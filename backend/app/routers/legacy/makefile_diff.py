from fastapi import APIRouter
from pathlib import Path
import difflib

router = APIRouter(prefix="/makefile", tags=["makefile"])

ROOT = Path(__file__).resolve().parents[3]
MAKEFILE = ROOT / "Makefile"
SNAPSHOT = ROOT / "data" / "Makefile.snapshot"


@router.get("/diff", summary="Get diff between current Makefile and snapshot")
def get_makefile_diff():
    if not MAKEFILE.exists():
        return {"lines": [], "error": "Makefile not found"}

    if not SNAPSHOT.exists():
        return {"lines": [], "error": "Snapshot not found"}

    current = MAKEFILE.read_text().splitlines()
    baseline = SNAPSHOT.read_text().splitlines()

    diff = difflib.ndiff(baseline, current)

    lines = []
    for d in diff:
        if d.startswith("+ "):
            lines.append({"type": "add", "text": d})
        elif d.startswith("- "):
            lines.append({"type": "remove", "text": d})
        else:
            lines.append({"type": "context", "text": d})

    return {"lines": lines}
