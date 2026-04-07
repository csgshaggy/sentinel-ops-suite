# app/routers/idrim_diff.py

from fastapi import APIRouter, Depends, HTTPException

from tools.security.idrim.idrim_service import IDRIMService
from tools.security.idrim.idrim_engine import IDRIMEngine
from tools.security.idrim.idrim_models import IDRIMRequest, IDRIMResult

router = APIRouter(prefix="/idrim/diff", tags=["IDRIM Diff"])


# Dependency providers
def get_service() -> IDRIMService:
    return IDRIMService()


def get_engine() -> IDRIMEngine:
    return IDRIMEngine()


@router.post("/", response_model=IDRIMResult)
async def idrim_diff(
    request: IDRIMRequest,
    service: IDRIMService = Depends(get_service),
    engine: IDRIMEngine = Depends(get_engine),
):
    """
    Compute a diff between the provided snapshot and the stored baseline.

    The IDRIMEngine handles:
      - baseline loading
      - snapshot normalization
      - diff computation
      - result packaging

    This endpoint is synchronous; SSE streaming is handled separately.
    """
    try:
        # Ensure baseline exists before diffing
        if not service.baseline_exists():
            raise HTTPException(
                status_code=400,
                detail="No baseline exists. Run /idrim/run to generate one.",
            )

        # Perform the diff
        result = engine.diff(request)
        return result

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
