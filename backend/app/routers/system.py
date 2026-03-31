import platform
import time

from fastapi import APIRouter

router = APIRouter()

START_TIME = time.time()


@router.get("/system/health")
async def system_health():
    return {"status": "ok"}


@router.get("/system/info")
async def system_info():
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "uptime_seconds": int(time.time() - START_TIME),
    }
