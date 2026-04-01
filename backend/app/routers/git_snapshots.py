from fastapi import APIRouter, Response
from pathlib import Path

router = APIRouter(prefix="/snapshots", tags=["Git Snapshots"])

HTML_PATH = Path("backend/app/reports/html/git_snapshot_latest.html")

@router.get("/latest", response_class=Response)
def get_latest_snapshot():
    if not HTML_PATH.exists():
        return Response("<h1>No snapshot HTML found</h1>", media_type="text/html")

    return Response(HTML_PATH.read_text(), media_type="text/html")
