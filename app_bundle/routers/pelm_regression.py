from fastapi import APIRouter
from backend.pelm.pelm_regression import analyze_regression

router = APIRouter(prefix="/pelm", tags=["PELM Regression"])


@router.get("/regression")
def pelm_regression():
    """
    Returns regression analytics across all PELM snapshots.
    Includes:
      - risk trend
      - risk delta
      - risk acceleration
      - drift detection
      - regression score (0–100)
    """
    return analyze_regression()
