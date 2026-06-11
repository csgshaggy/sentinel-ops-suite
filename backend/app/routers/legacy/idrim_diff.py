# app/routers/idrim_diff.py

from fastapi import APIRouter, Depends, HTTPException

from tools.security.idrim.idrim_service import IDRIMService
from tools.security.idrim.idrim_engine import IDRIMEngine
from tools.security.idrim.idrim_models import IDRIMRequest, IDRIMResult

router = APIRouter(prefix="/idrim/diff", tags=["IDRIM Diff"])


# Dependency injection for service + engine
def get_service():
    return IDRIMService()


def get_engine():
    return IDRIMEngine()


@router.post("/", response_model=IDRIMResult)
async def idrim_diff(
    request: IDRIMRequest,
    service: IDRIMService = Depends(get_service),
    engine: IDRIMEngine = Depends(get_engine),
):
    """
    Perform a diff between the incoming snapshot and the stored baseline.

    The engine handles:
      - baseline loading
      - snapshot normalization
      - diff computation
      - result packaging
    """
    try:
        # Ensure baseline exists
        if not service.baseline_exists():
            raise HTTPException(
                status_code=400,
                detail="No baseline exists. Run /idrim/run to generate one.",
            )

        # Compute diff
        result = engine.diff(request)
        return result

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
