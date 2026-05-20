# backend/tools/security/idrim/idrim_tasks.py

from typing import Dict, Any

from .idrim_service import IDRIMService


class IDRIMTaskRunner:
    """
    Task runner for scheduled or on-demand IDRIM analyses.
    """

    def __init__(self, storage_path: str = "data/idrim"):
        self.service = IDRIMService(storage_path=storage_path)

    async def run_analysis(self, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "source": "task_runner",
            "scope": "snapshot",
            "payload": snapshot,
        }
        return await self.service.execute(payload)
