# app/routers/makefile_admin.py

from fastapi import APIRouter, HTTPException

from app.utils.file_utils import (
    compute_health_score,
    ensure_reference_makefile,
    file_exists,
    read_file_lines,
    unified_diff,
)

router = APIRouter()

MAKEFILE_PATH = "backend/Makefile"
REFERENCE_PATH = "backend/Makefile.reference"


# ------------------------------------------------------------
# GET /api/makefile
# ------------------------------------------------------------
@router.get("/makefile")
async def get_makefile():
    """
    Return the current Makefile contents.
    """
    try:
        lines = read_file_lines(MAKEFILE_PATH)
        return {"path": MAKEFILE_PATH, "lines": lines}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ------------------------------------------------------------
# GET /api/makefile/reference
# ------------------------------------------------------------
@router.get("/makefile/reference")
async def get_reference_makefile():
    """
    Return the reference Makefile used for diffing.
    """
    if not file_exists(REFERENCE_PATH):
        return {
            "path": None,
            "lines": [],
            "warning": "Reference Makefile not found. Generate it using POST /api/makefile/reference/regenerate.",
        }

    lines = read_file_lines(REFERENCE_PATH)
    return {"path": REFERENCE_PATH, "lines": lines}


# ------------------------------------------------------------
# POST /api/makefile/reference/regenerate
# ------------------------------------------------------------
@router.post("/makefile/reference/regenerate")
async def regenerate_reference():
    """
    Regenerate backend/Makefile.reference from backend/Makefile.
    """
    try:
        info = ensure_reference_makefile()
        return {"status": "ok", **info}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ------------------------------------------------------------
# GET /api/makefile/diff
# ------------------------------------------------------------
@router.get("/makefile/diff")
async def get_makefile_diff():
    """
    Return a unified diff between the current Makefile and the reference.
    """
    try:
        current = read_file_lines(MAKEFILE_PATH)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    if not file_exists(REFERENCE_PATH):
        return {
            "diff": [],
            "health": 100,
            "warning": "Reference Makefile not found. Generate it using POST /api/makefile/reference/regenerate.",
        }

    reference = read_file_lines(REFERENCE_PATH)
    diff_lines = unified_diff(current, reference)
    health = compute_health_score(diff_lines)

    return {"diff": diff_lines, "health": health}


# ------------------------------------------------------------
# GET /api/makefile/health
# ------------------------------------------------------------
@router.get("/makefile/health")
async def get_makefile_health():
    """
    Return only the health score for the Makefile.
    """
    try:
        current = read_file_lines(MAKEFILE_PATH)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    if not file_exists(REFERENCE_PATH):
        return {
            "health": 100,
            "warning": "Reference Makefile not found. Generate it using POST /api/makefile/reference/regenerate.",
        }

    reference = read_file_lines(REFERENCE_PATH)
    diff_lines = unified_diff(current, reference)
    health = compute_health_score(diff_lines)

    return {"health": health}
