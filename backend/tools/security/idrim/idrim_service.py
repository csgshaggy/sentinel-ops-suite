"""
IDRIM Service Layer
-------------------
This module provides the orchestration layer between the IDRIMEngine,
IDRIMTaskRunner, and external callers (API router, CLI, scheduled jobs).

The service is intentionally thin, deterministic, and operator‑grade:
- No hidden state
- No implicit caching
- All operations return IDRIMResult objects
- All failures raise explicit IDRIM exceptions
"""

from __future__ import annotations

import logging
from typing import Optional

from .idrim_engine import IDRIMEngine
from .idrim_tasks import IDRIMTaskRunner
from .idrim_models import IDRIMRequest, IDRIMResult
from .idrim_exceptions import (
    IDRIMEngineError,
    IDRIMTaskError,
    IDRIMInvalidRequestError,
)

logger = logging.getLogger(__name__)


class IDRIMService:
    """
    High‑level orchestration service for IDRIM operations.

    Responsibilities:
    - Validate incoming requests
    - Delegate execution to IDRIMEngine
    - Optionally run async/parallel tasks via IDRIMTaskRunner
    - Normalize all outputs into IDRIMResult
    """

    def __init__(
        self,
        engine: Optional[IDRIMEngine] = None,
        task_runner: Optional[IDRIMTaskRunner] = None,
    ) -> None:
        self.engine = engine or IDRIMEngine()
        self.task_runner = task_runner or IDRIMTaskRunner()

        logger.debug("IDRIMService initialized with engine=%s task_runner=%s",
                     type(self.engine).__name__,
                     type(self.task_runner).__name__)

    # ----------------------------------------------------------------------
    # Validation
    # ----------------------------------------------------------------------
    def _validate_request(self, request: IDRIMRequest) -> None:
        if not isinstance(request, IDRIMRequest):
            raise IDRIMInvalidRequestError(
                f"Expected IDRIMRequest, got {type(request).__name__}"
            )

        if not request.target_path:
            raise IDRIMInvalidRequestError("IDRIMRequest missing target_path")

        logger.debug("Validated IDRIMRequest: %s", request)

    # ----------------------------------------------------------------------
    # Synchronous Execution
    # ----------------------------------------------------------------------
    def run(self, request: IDRIMRequest) -> IDRIMResult:
        """
        Execute a single IDRIM analysis synchronously.
        """
        self._validate_request(request)

        logger.info("IDRIMService.run invoked for target: %s", request.target_path)

        try:
            result = self.engine.run_analysis(request)
        except Exception as exc:
            logger.exception("Engine failure during run_analysis")
            raise IDRIMEngineError(str(exc)) from exc

        if not isinstance(result, IDRIMResult):
            raise IDRIMEngineError(
                f"Engine returned invalid type: {type(result).__name__}"
            )

        logger.debug("IDRIMService.run completed with result: %s", result)
        return result

    # ----------------------------------------------------------------------
    # Asynchronous / Parallel Execution
    # ----------------------------------------------------------------------
    async def run_async(self, request: IDRIMRequest) -> IDRIMResult:
        """
        Execute an IDRIM analysis asynchronously using the task runner.
        """
        self._validate_request(request)

        logger.info("IDRIMService.run_async invoked for target: %s", request.target_path)

        try:
            result = await self.task_runner.run_task(self.engine, request)
        except Exception as exc:
            logger.exception("Task runner failure during run_async")
            raise IDRIMTaskError(str(exc)) from exc

        if not isinstance(result, IDRIMResult):
            raise IDRIMTaskError(
                f"TaskRunner returned invalid type: {type(result).__name__}"
            )

        logger.debug("IDRIMService.run_async completed with result: %s", result)
        return result

    # ----------------------------------------------------------------------
    # Health / Diagnostics
    # ----------------------------------------------------------------------
    def health(self) -> dict:
        """
        Lightweight health check for dashboards and CI.
        """
        status = {
            "engine": self.engine.health(),
            "task_runner": self.task_runner.health(),
            "service": "ok",
        }

        logger.debug("IDRIMService.health: %s", status)
        return status
