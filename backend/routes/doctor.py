from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from tools.super_doctor import run_super_doctor

router = APIRouter(
    prefix="/admin/doctor",
    tags=["admin", "doctor"],
)


@router.get("/", response_model=dict)
def get_doctor_summary() -> Dict[str, Any]:
    """
    Run the Super Doctor and return structured diagnostic results.
    This endpoint is used by dashboards, admin panels, and CI systems.
    """
    return run_super_doctor({})
