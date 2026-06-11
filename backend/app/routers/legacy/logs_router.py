# /home/ubuntu/sentinel-ops-suite/backend/app/routers/logs_router.py
# SentinelOps — Streaming Logs Router (SSE Heartbeat Stream)

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import time

# ---------------------------------------------------------
# Router prefix (no /api here — main.py applies prefix="/api")
# Final path becomes /api/stream/logs
# ---------------------------------------------------------
router = APIRouter(prefix="/stream", tags=["Streaming"])


# ---------------------------------------------------------
# Heartbeat Log Stream Generator (SSE)
# ---------------------------------------------------------
def log_stream():
    while True:
        yield f"data: heartbeat {time.time()}\n\n"
        time.sleep(1)


# ---------------------------------------------------------
# Stream Logs (SSE)
# ---------------------------------------------------------
@router.get("/logs")
def stream_logs():
    return StreamingResponse(log_stream(), media_type="text/event-stream")
