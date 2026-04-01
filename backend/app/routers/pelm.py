from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/pelm", tags=["PELM"])


# ------------------------------------------------------------
# Schemas
# ------------------------------------------------------------

class PelmEvent(BaseModel):
    timestamp: str
    identity: str
    action: str
    severity: str
    details: Dict[str, Any]


class PelmSummary(BaseModel):
    total_events: int
    high_risk_identities: int
    lateral_movement_attempts: int
    privilege_escalations: int
    drift_score: float


class PelmRisk(BaseModel):
    identity: str
    risk_score: float
    reasons: List[str]


class PelmGraph(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]


# ------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------

@router.get("/events", response_model=List[PelmEvent])
def get_pelm_events():
    # Placeholder — will be wired to your PELM engine
    return []


@router.get("/summary", response_model=PelmSummary)
def get_pelm_summary():
    return PelmSummary(
        total_events=0,
        high_risk_identities=0,
        lateral_movement_attempts=0,
        privilege_escalations=0,
        drift_score=0.0,
    )


@router.get("/risks", response_model=List[PelmRisk])
def get_pelm_risks():
    return []


@router.get("/graph", response_model=PelmGraph)
def get_pelm_graph():
    return PelmGraph(nodes=[], edges=[])
