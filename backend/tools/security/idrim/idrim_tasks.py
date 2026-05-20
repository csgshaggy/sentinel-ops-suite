"""
IDRIM Task Runner
-----------------
Async/parallel orchestration for IDRIMEngine operations.

This module is intentionally minimal and deterministic:
- No global state
- No background daemons
- All entrypoints are explicit methods
"""

from __future__ import annotations

import asyncio
import logging
from typing import Iterable, List

from .idrim_engine import IDRIMEngine
from .idrim_models import IDRIMRequest, IDRIMResult
from .idrim_exceptions import IDRIMTaskError

logger = logging.getLogger(__name__)


class IDRIMTaskRunner:
    """
    Thin async orchestration layer for IDRIMEngine.

    Responsibilities:
    - Run a single request in an async context
    - Run multiple requests concurrently with bounded fan‑out
    - Expose a simple health() surface for dashboards/CI
    """

    def __init__(self, max_concurrency: int = 5) -> None:
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be >= 1")

        self.max_concurrency = max_concurrency
        logger.debug("IDRIMTaskRunner initialized with max_concurrency=%d",
                     self.max_concurrency)

    # ------------------------------------------------------------------ #
    # Health                                                             #
    # ------------------------------------------------------------------ #
    def health(self) -> dict:
        """
        Lightweight health snapshot for dashboards and CI.
        """
        status = {
            "status": "ok",
            "max_concurrency": self.max_concurrency,
        }
        logger.debug("IDRIMTaskRunner.health: %s", status)
        return status

    # ------------------------------------------------------------------ #
    # Core async execution                                               #
    # ------------------------------------------------------------------ #
    async def run_task(
        self,
        engine: IDRIMEngine,
        request: IDRIMRequest,
    ) -> IDRIMResult:
        """
        Run a single IDRIM request using the provided engine in an async context.

        This is the primitive used by IDRIMService.run_async().
        """
        logger.info(
            "IDRIMTaskRunner.run_task invoked for target=%s using engine=%s",
            getattr(request, "target_path", "<unknown>"),
            type(engine).__name__,
        )

        loop = asyncio.get_running_loop()

        try:
            # Offload the synchronous engine call to a thread to avoid
            # blocking the event loop.
            result = await loop.run_in_executor(
                None,
                engine.run_analysis,
                request,
            )
        except Exception as exc:
            logger.exception("IDRIMTaskRunner.run_task failed")
            raise IDRIMTaskError(str(exc)) from exc

        if not isinstance(result, IDRIMResult):
            raise IDRIMTaskError(
                f"Engine returned invalid type from run_analysis: {type(result).__name__}"
            )

        logger.debug("IDRIMTaskRunner.run_task completed with result=%s", result)
        return result

    # ------------------------------------------------------------------ #
    # Batch / concurrent execution                                       #
    # ------------------------------------------------------------------ #
    async def run_many(
        self,
        engine: IDRIMEngine,
        requests: Iterable[IDRIMRequest],
    ) -> List[IDRIMResult]:
        """
        Run multiple IDRIM requests concurrently with bounded fan‑out.

        Returns a list of IDRIMResult in the same order as the input requests.
        Any failure raises IDRIMTaskError and cancels remaining tasks.
        """
        requests_list = list(requests)
        logger.info(
            "IDRIMTaskRunner.run_many invoked for %d requests using engine=%s",
            len(requests_list),
            type(engine).__name__,
        )

        semaphore = asyncio.Semaphore(self.max_concurrency)

        async def _guarded_run(req: IDRIMRequest) -> IDRIMResult:
            async with semaphore:
                return await self.run_task(engine, req)

        tasks = [asyncio.create_task(_guarded_run(req)) for req in requests_list]

        try:
            results = await asyncio.gather(*tasks)
        except Exception as exc:
            logger.exception("IDRIMTaskRunner.run_many encountered failure, cancelling remaining tasks")
            for t in tasks:
                if not t.done():
                    t.cancel()
            raise IDRIMTaskError(str(exc)) from exc

        logger.debug(
            "IDRIMTaskRunner.run_many completed with %d results",
            len(results),
        )
        return results
