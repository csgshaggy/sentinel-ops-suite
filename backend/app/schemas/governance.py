from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class GovernanceRunRequest(BaseModel):
    repo_id: int
    mode: Literal["github", "local"] = "github"
    ref: Optional[str] = "main"

class GovernanceRunResponse(BaseModel):
    run_id: int
    status: str
    triggered_at: datetime
