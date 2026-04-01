from typing import Any, Dict, List

from pydantic import BaseModel


class PelmDashboardEvent(BaseModel):
    timestamp: str
    identity: str
    action: str
    severity: str
    details: Dict[str, Any]


class PelmDashboardSummary(BaseModel):
    drift_score: float
    high_risk_identities: int
    lateral_movement_attempts: int
    privilege_escalations: int
    total_events: int


class PelmDashboardRiskItem(BaseModel):
    identity: str
    risk_score: float
    reasons: List[str]


class PelmDashboardGraph(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
