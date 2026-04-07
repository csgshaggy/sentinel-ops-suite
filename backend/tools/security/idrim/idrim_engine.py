"""
IDRIM Engine
------------
Core analysis engine for IDRIM operations.

This module performs the actual inspection, scoring, and result
generation for a given IDRIMRequest. It is intentionally deterministic,
side‑effect‑free, and suitable for both synchronous and async execution.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from .idrim_models import IDRIMRequest, IDRIMResult
from .idrim_exceptions import (
    IDRIMEngineError,
    IDRIMInvalidRequestError,
)

logger = logging.getLogger(__name__)


class IDRIMEngine:
    """
    Core IDRIM analysis engine.

    Responsibilities:
    - Validate request inputs
    - Perform deterministic inspection of the target path
    - Produce an IDRIMResult object
    - Expose a health() surface for dashboards/CI
    """

    def __init__(self) -> None:
        logger.debug("IDRIMEngine initialized")

    # ------------------------------------------------------------------ #
    # Health                                                             #
    # ------------------------------------------------------------------ #
    def health(self) -> dict:
        """
        Lightweight health snapshot for dashboards and CI.
        """
        status = {
            "status": "ok",
            "engine": "IDRIMEngine",
        }
        logger.debug("IDRIMEngine.health: %s", status)
        return status

    # ------------------------------------------------------------------ #
    # Validation                                                         #
    # ------------------------------------------------------------------ #
    def _validate(self, request: IDRIMRequest) -> Path:
        if not isinstance(request, IDRIMRequest):
            raise IDRIMInvalidRequestError(
                f"Expected IDRIMRequest, got {type(request).__name__}"
            )

        if not request.target_path:
            raise IDRIMInvalidRequestError("IDRIMRequest missing target_path")

        path = Path(request.target_path).expanduser().resolve()

        if not path.exists():
            raise IDRIMInvalidRequestError(f"Target path does not exist: {path}")

        logger.debug("IDRIMEngine validated request: %s", request)
        return path

    # ------------------------------------------------------------------ #
    # Core Analysis                                                      #
    # ------------------------------------------------------------------ #
    def run_analysis(self, request: IDRIMRequest) -> IDRIMResult:
        """
        Perform the core IDRIM analysis.

        This implementation is intentionally simple and deterministic.
        Real logic can be layered in without changing the service/task API.
        """
        logger.info("IDRIMEngine.run_analysis invoked for %s", request.target_path)

        try:
            path = self._validate(request)
        except Exception as exc:
            logger.exception("Validation failure in IDRIMEngine")
            raise

        try:
            # Example deterministic inspection:
            file_count = 0
            dir_count = 0

            if path.is_file():
                file_count = 1
            else:
                for item in path.rglob("*"):
                    if item.is_file():
                        file_count += 1
                    elif item.is_dir():
                        dir_count += 1

            # Example scoring logic (placeholder)
            score = min(100, file_count + dir_count)

            result = IDRIMResult(
                target=str(path),
                file_count=file_count,
                dir_count=dir_count,
                score=score,
                metadata={"engine": "IDRIMEngine"},
            )

        except Exception as exc:
            logger.exception("Engine failure during analysis")
            raise IDRIMEngineError(str(exc)) from exc

        logger.debug("IDRIMEngine.run_analysis completed with result: %s", result)
        return result
