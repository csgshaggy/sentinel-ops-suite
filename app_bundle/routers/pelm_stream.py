from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/pelm/stream", tags=["pelm"])


async def stream():
    yield "pelm-stream-start\n"
    yield "pelm-stream-end\n"


@router.get("/")
async def pelm_stream():
    return StreamingResponse(stream(), media_type="text/plain")
