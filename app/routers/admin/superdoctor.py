from fastapi import APIRouter
from pathlib import Path

from app.utils.modes import Mode
from tools.super_doctor_runner import run_super_doctor

router = APIRouter(prefix="/superdoctor", tags=["superdoctor"])


@router.get("/run")
def run_superdoctor_endpoint(mode: str = "LOCAL", project_root: str = "."):
    m = Mode[mode.upper()]
    results, summary, timings = run_super_doctor(
        project_root=Path(project_root), mode=m
    )

    return {
        "summary": summary.__dict__,
        "timings_ms": timings,
        "results": {
            pid: [r.__dict__ for r in checks] for pid, checks in results.items()
        },
    }
