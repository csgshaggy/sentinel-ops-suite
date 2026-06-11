from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import time, random, json

router = APIRouter(prefix="/stream", tags=["Streaming"])

def ops_stream():
    while True:
        payload = {
            "type": "heartbeat",
            "timestamp": time.time(),
        }
        yield f"data: {json.dumps(payload)}\n\n"

        payload = {
            "type": "anomaly",
            "score": random.randint(0, 100),
        }
        yield f"data: {json.dumps(payload)}\n\n"

        payload = {
            "type": "idrim",
            "drift": random.choice(["none", "low", "high"]),
        }
        yield f"data: {json.dumps(payload)}\n\n"

        payload = {
            "type": "pelm",
            "risk": random.randint(1, 5),
        }
        yield f"data: {json.dumps(payload)}\n\n"

        time.sleep(1)

@router.get("/ops")
def stream_ops():
    return StreamingResponse(ops_stream(), media_type="text/event-stream")
