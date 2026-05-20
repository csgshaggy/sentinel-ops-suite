from __future__ import annotations

import time
from typing import Any, Dict

from fastapi import APIRouter

router = APIRouter(prefix="/admin/timers", tags=["admin-timers"])


# ------------------------------------------------------------
# Internal timing utilities
# ------------------------------------------------------------

START_TIME = time.monotonic()


def _now_ms() -> int:
    return int(time.time() * 1000)


def _uptime_seconds() -> float:
    return round(time.monotonic() - START_TIME, 3)


def _timestamp_info() -> Dict[str, Any]:
    """
    Provide a consistent snapshot of timing information.
    """
    return {
        "epoch_seconds": time.time(),
        "epoch_ms": _now_ms(),
        "uptime_seconds": _uptime_seconds(),
        "localtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
    }


# ------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------


@router.get("/now", summary="Return current timestamp information")
def get_current_time() -> Dict[str, Any]:
    """
    Return a structured view of current time, uptime, and clock state.
    """
    return {
        "success": True,
        "data": _timestamp_info(),
    }


@router.get("/uptime", summary="Return process uptime in seconds")
def get_uptime() -> Dict[str, Any]:
    """
    Return the number of seconds the process has been running.
    """
    return {
        "success": True,
        "uptime_seconds": _uptime_seconds(),
    }


@router.get("/sleep/{ms}", summary="Perform a controlled sleep (for testing)")
def sleep_for(ms: int) -> Dict[str, Any]:
    """
    Sleep for a specified number of milliseconds.
    Useful for testing async behavior, latency, and timing.
    """
    if ms < 0:
        return {
            "success": False,
            "error": "Sleep duration must be non-negative",
        }

    seconds = ms / 1000.0

    try:
        time.sleep(seconds)
    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }

    return {
        "success": True,
        "slept_ms": ms,
        "after": _timestamp_info(),
    }
