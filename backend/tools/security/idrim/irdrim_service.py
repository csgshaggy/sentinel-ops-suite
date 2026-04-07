# backend/tools/security/idrim/idrim_service.py

import asyncio
from typing import Dict, Any, List

from .idrim_engine import IDRIMEngine
from .idrim_models import IDRIMSnapshot, IDRIMRequest, IDRIMResult
from .idrim_exceptions import (
    IDRIMBaseException,
    IDRIMValidationError,
    IDRIMServiceError,
)


class IDRIMService:
    """
    Service layer around the IDRIMEngine.
    Handles requests, validation, and SSE subscriptions.
    """

    def __init__(self, storage_path: str = "data/idrim"):
        self.engine = IDRIMEngine(storage_path=storage_path)
        self._subscribers: List[asyncio.Queue] = []

    # ------------- SSE subscription -------------

    def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        self._subscribers.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue) -> None:
        if q in self._subscribers:
            self._subscribers.remove(q)

    async def _broadcast(self, event: Dict[str, Any]) -> None:
        for q in list(self._subscribers):
            await q.put(event)

    # ------------- Health -------------

    def health_check(self) -> Dict[str, Any]:
        try:
            exists = self.engine.baseline_exists()
            return {"status": "ok", "baseline_exists": exists}
        except Exception as exc:
            raise IDRIMServiceError(f"Health check failed: {exc}")

    # ------------- Execute -------------

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            req = IDRIMRequest(**payload)
        except Exception as exc:
            raise IDRIMValidationError(f"Invalid payload: {exc}")

        snapshot_data = req.payload or {}
        snapshot = IDRIMSnapshot(**snapshot_data)

        try:
            result = self.engine.analyze(snapshot)
        except IDRIMBaseException:
            raise
        except Exception as exc:
            raise IDRIMServiceError(f"Engine execution failed: {exc}")

        out = IDRIMResult(success=True, details=result.dict())
        await self._broadcast({"type": "idrim_analysis", "data": out.dict()})
        return out.dict()
