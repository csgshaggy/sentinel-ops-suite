"""
IDRIM FastAPI Router
--------------------
Thin API layer exposing IDRIM operations.

This router is intentionally:
- Deterministic
- Explicit
- Free of business logic
- Bound only to IDRIMService
"""

from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException

from .idrim_service import IDRIMService
from .idrim_models import IDRIMRequest, IDRIMResult
from .idrim_exceptions import (
    IDRIMError,
    IDRIMInvalidRequestError,
    IDRIMEngineError,
    IDRIMTaskError,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/idrim", tags=["IDRIM"])
service = IDRIMService()


# ----------------------------------------------------------------------
# Health Endpoint
# ----------------------------------------------------------------------
@router.get("/health")
def idrim_health() -> dict:
    """
    Lightweight health snapshot for dashboards and CI.
    """
    try:
        return service.health()
    except Exception as exc:
        logger.exception("IDRIM health check failed")
        raise HTTPException(status_code=500, detail=str(exc))


# ----------------------------------------------------------------------
# Synchronous Execution
# ----------------------------------------------------------------------
@router.post("/run", response_model=IDRIMResult)
def idrim_run(request: IDRIMRequest) -> IDRIMResult:
    """
    Execute a synchronous IDRIM analysis.
    """
    try:
        return service.run(request)
    except IDRIMInvalidRequestError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except IDRIMEngineError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except IDRIMError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        logger.exception("Unexpected failure in /idrim/run")
        raise HTTPException(status_code=500, detail=str(exc))


# ----------------------------------------------------------------------
# Asynchronous Execution
# ----------------------------------------------------------------------
@router.post("/run-async", response_model=IDRIMResult)
async def idrim_run_async(request: IDRIMRequest) -> IDRIMResult:
    """
    Execute an asynchronous IDRIM analysis.
    """
    try:
        return await service.run_async(request)
    except IDRIMInvalidRequestError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except IDRIMTaskError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except IDRIMError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        logger.exception("Unexpected failure in /idrim/run-async")
        raise HTTPException(status_code=500, detail=str(exc))
