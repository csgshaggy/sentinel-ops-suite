from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json
from datetime import datetime

router = APIRouter(prefix="/pelm/events", tags=["PELM Stream"])


async def event_stream():
    while True:
        # Placeholder event — will be replaced with real PELM engine output
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "identity": "placeholder",
            "action": "noop",
            "severity": "info",
            "details": {"msg": "stream heartbeat"},
        }

        yield f"data: {json.dumps(event)}\n\n"
        await asyncio.sleep(1)


@router.get("/stream")
async def pelm_event_stream():
    return StreamingResponse(event_stream(), media_type="text/event-stream")
