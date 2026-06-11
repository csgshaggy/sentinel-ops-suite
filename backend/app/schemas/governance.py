# /app/schemas/governance.py
# SentinelOps – Governance API Schemas

from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


# -------------------------------------------------
# Request: Trigger Governance Run
# -------------------------------------------------
class GovernanceRunRequest(BaseModel):
    repo_id: int
    mode: Literal["github", "local"] = "github"
    ref: Optional[str] = "main"


# -------------------------------------------------
# Response: Governance Run Triggered
# -------------------------------------------------
class GovernanceRunResponse(BaseModel):
    run_id: int
    status: str
    triggered_at: datetime


# -------------------------------------------------
# Response: Latest Governance Posture
# -------------------------------------------------
class LatestGovernanceResponse(BaseModel):
    run_id: int
    repo_id: int
    status: str
    score: int
    violations_count: int
    triggered_at: datetime
    completed_at: Optional[datetime]


# -------------------------------------------------
# Response: Workflow Status (for /workflows route)
# -------------------------------------------------
class WorkflowStatus(BaseModel):
    workflow_id: int
    repo_id: int
    path: str
    status: str
    violations_count: int
    last_validated_at: Optional[datetime]
