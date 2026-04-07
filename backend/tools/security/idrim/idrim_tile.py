"""
IDRIM Dashboard Tile
--------------------
Provides a deterministic JSON payload suitable for a dashboard tile.

This module is intentionally:
- Stateless
- Fast
- CI‑safe
- Free of business logic (delegates to IDRIMService)
"""

from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException

from .idrim_service import IDRIMService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/idrim", tags=["IDRIM"])
service = IDRIMService()


@router.get("/tile")
def idrim_tile() -> dict:
    """
    Returns a compact dashboard‑friendly snapshot of IDRIM health.

    This is typically consumed by:
    - Operator consoles
    - Cyber‑ops dashboards
    - Health tiles
    - CI status boards
    """
    try:
        health = service.health()

        return {
            "title": "IDRIM",
            "status": health.get("service", "unknown"),
            "engine": health.get("engine", {}),
            "task_runner": health.get("task_runner", {}),
        }

    except Exception as exc:
        logger.exception("IDRIM tile generation failed")
        raise HTTPException(status_code=500, detail=str(exc))
