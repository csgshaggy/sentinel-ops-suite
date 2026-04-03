from __future__ import annotations

import threading
from typing import Any, Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/admin/locks", tags=["admin-locks"])


# ------------------------------------------------------------
# Internal lock registry
# ------------------------------------------------------------


class LockRegistry:
    """
    A simple in‑memory registry for named locks.
    This allows the admin panel to inspect lock state safely.
    """

    def __init__(self) -> None:
        self._locks: Dict[str, threading.Lock] = {}
        self._lock = threading.Lock()

    def get_or_create(self, name: str) -> threading.Lock:
        with self._lock:
            if name not in self._locks:
                self._locks[name] = threading.Lock()
            return self._locks[name]

    def list_locks(self) -> List[str]:
        with self._lock:
            return sorted(self._locks.keys())

    def describe(self, name: str) -> Dict[str, Any]:
        lock = self._locks.get(name)
        if lock is None:
            return {"exists": False, "name": name}

        # Python's Lock doesn't expose much state, but we can infer some things.
        locked = lock.locked()

        return {
            "exists": True,
            "name": name,
            "locked": locked,
            "type": type(lock).__name__,
        }


lock_registry = LockRegistry()


# ------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------


@router.get("/list", summary="List all known locks")
def list_locks() -> Dict[str, Any]:
    """
    Return a list of all lock names currently registered.
    """
    return {
        "count": len(lock_registry.list_locks()),
        "locks": lock_registry.list_locks(),
    }


@router.get("/describe/{name}", summary="Describe a specific lock")
def describe_lock(name: str) -> Dict[str, Any]:
    """
    Return information about a specific lock.
    """
    return lock_registry.describe(name)


@router.post("/acquire/{name}", summary="Acquire a named lock (non-blocking)")
def acquire_lock(name: str) -> Dict[str, Any]:
    """
    Attempt to acquire a lock without blocking.
    Useful for debugging concurrency issues.
    """
    lock = lock_registry.get_or_create(name)

    acquired = False
    try:
        acquired = lock.acquire(blocking=False)
    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "name": name,
        }

    return {
        "success": acquired,
        "name": name,
        "locked": lock.locked(),
    }


@router.post("/release/{name}", summary="Release a named lock")
def release_lock(name: str) -> Dict[str, Any]:
    """
    Release a lock if it is currently held.
    """
    lock = lock_registry.get_or_create(name)

    if not lock.locked():
        return {
            "success": False,
            "name": name,
            "error": "Lock is not currently held",
        }

    try:
        lock.release()
    except Exception as exc:
        return {
            "success": False,
            "name": name,
            "error": str(exc),
        }

    return {
        "success": True,
        "name": name,
        "locked": lock.locked(),
    }
