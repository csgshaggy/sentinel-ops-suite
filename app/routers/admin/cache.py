from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict

import psutil
from fastapi import APIRouter
import socket
import sys
import time

router = APIRouter(prefix="/admin/cache", tags=["admin-cache"])


def _now_ms() -> int:
    return int(time.time() * 1000)


class CacheStats:
    def __init__(self) -> None:
        self.started_at_ms = _now_ms()

    def to_dict(self) -> Dict[str, Any]:
        process = psutil.Process()
        memory_info = process.memory_info()

        return {
            "python_version": sys.version,
            "hostname": socket.gethostname(),
            "uptime_ms": _now_ms() - self.started_at_ms,
            "memory_rss_bytes": memory_info.rss,
            "memory_vms_bytes": memory_info.vms,
        }


cache_stats = CacheStats()


@lru_cache(maxsize=1)
def get_cached_stats() -> Dict[str, Any]:
    # This is intentionally simple: it demonstrates caching behavior
    # and is safe to call from multiple endpoints.
    return cache_stats.to_dict()


@router.get("/stats", summary="Get cached admin cache stats")
def read_cache_stats() -> Dict[str, Any]:
    """
    Return cached view of basic process and host information.

    This endpoint is intentionally lightweight and safe to call frequently.
    """
    return {
        "cached": True,
        "data": get_cached_stats(),
    }


@router.get("/stats/refresh", summary="Refresh and return cache stats")
def refresh_cache_stats() -> Dict[str, Any]:
    """
    Refresh the cached stats and return the new values.
    """
    # Clear the lru_cache and recompute
    get_cached_stats.cache_clear()  # type: ignore[attr-defined]
    data = get_cached_stats()
    return {
        "cached": False,
        "data": data,
    }
