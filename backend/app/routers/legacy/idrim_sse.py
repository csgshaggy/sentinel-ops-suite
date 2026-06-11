from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/idrim", tags=["IDRIM SSE"])

tasks = IDRIMTaskRunner()


def _event_stream(task_id: str):
    """
    Generator that yields Server-Sent Events (SSE) for a given task_id.
    """
    try:
        for event in tasks.stream_events(task_id):
            yield f"data: {event}\n\n"
    except Exception as exc:
        # In SSE, we can't raise HTTPException mid-stream, so we emit an error event.
        yield f"data: {{\"error\": \"{str(exc)}\"}}\n\n"


@router.get("/stream/{task_id}")
async def idrim_stream(task_id: str):
    """
    SSE endpoint for streaming IDRIM task progress and results.
    """
    # Optional: validate task exists before streaming
    status = tasks.get_status(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return StreamingResponse(
        _event_stream(task_id),
        media_type="text/event-stream",
    )
from tools.security.idrim.idrim_tasks import IDRIMTaskRunner
