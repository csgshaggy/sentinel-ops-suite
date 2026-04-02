from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import time

router = APIRouter(prefix="/stream", tags=["Streaming"])

def log_stream():
    while True:
        yield f"data: heartbeat {time.time()}\n\n"
        time.sleep(1)

@router.get("/logs")
def stream_logs():
    return StreamingResponse(log_stream(), media_type="text/event-stream")
