import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from tools.plugins.pelm import stream_pelm_events

router = APIRouter(prefix="/pelm/events", tags=["PELM Stream"])


async def event_generator():
    """
    SSE generator for live PELM events.
    Yields events as they occur.
    """
    async for event in stream_pelm_events():
        yield f"data: {event}\n\n"
        await asyncio.sleep(0.1)


@router.get("/stream")
async def pelm_event_stream():
    """
    Server-Sent Events endpoint for live PELM event streaming.
    """
    return StreamingResponse(event_generator(), media_type="text/event-stream")
