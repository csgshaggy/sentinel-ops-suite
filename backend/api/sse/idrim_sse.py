# backend/api/sse/idrim_sse.py

import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.tools.security.idrim.idrim_service import IDRIMService

router = APIRouter(prefix="/idrim/sse", tags=["IDRIM-SSE"])
service = IDRIMService()


async def event_stream():
    queue = service.subscribe()
    try:
        while True:
            event = await queue.get()
            yield f"data: {event}\n\n"
            await asyncio.sleep(0)
    except asyncio.CancelledError:
        service.unsubscribe(queue)
        raise


@router.get("/events")
async def idrim_events():
    return StreamingResponse(event_stream(), media_type="text/event-stream")
