"""
IDRIM SSE Stream
----------------
Server‑Sent Events (SSE) endpoint for streaming IDRIM health and
lightweight telemetry to dashboards.

This module is intentionally:
- Deterministic
- Stateless
- Safe for long‑running connections
"""

from __future__ import annotations

import asyncio
import json
import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from .idrim_service import IDRIMService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/idrim", tags=["IDRIM"])
service = IDRIMService()


async def _event_stream(interval: float = 2.0):
    """
    Async generator that yields IDRIM health snapshots every `interval` seconds.
    """
    while True:
        try:
            payload = service.health()
            data = json.dumps(payload)
            yield f"data: {data}\n\n"
        except Exception as exc:
            logger.exception("IDRIM SSE stream failure: %s", exc)
            yield f"data: {json.dumps({'error': str(exc)})}\n\n"

        await asyncio.sleep(interval)


@router.get("/stream")
async def idrim_stream():
    """
    SSE endpoint for dashboards.
    """
    return StreamingResponse(
        _event_stream(),
        media_type="text/event-stream",
    )
