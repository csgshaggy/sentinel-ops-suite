# backend/api/routes/idrim_router.py

from fastapi import APIRouter, HTTPException
from backend.tools.security.idrim.idrim_service import IDRIMService
from backend.tools.security.idrim.idrim_exceptions import (
    IDRIMBaseException,
    IDRIMValidationError,
    IDRIMEngineStateError,
    IDRIMTaskExecutionError,
    IDRIMServiceError,
)

router = APIRouter(prefix="/idrim", tags=["IDRIM"])
service = IDRIMService()


@router.get("/health")
async def idrim_health():
    try:
        return service.health_check()
    except IDRIMBaseException as exc:
        raise HTTPException(status_code=500, detail=exc.to_dict())


@router.post("/run")
async def idrim_run(payload: dict):
    try:
        return await service.execute(payload)
    except IDRIMValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.to_dict())
    except (IDRIMEngineStateError, IDRIMTaskExecutionError, IDRIMServiceError) as exc:
        raise HTTPException(status_code=500, detail=exc.to_dict())
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"error": "idrim_unexpected_error", "message": str(exc)},
        )
