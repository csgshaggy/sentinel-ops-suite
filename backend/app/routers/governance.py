# /app/routers/governance.py
# SentinelOps – Governance API Router

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.governance import (
    GovernanceRunRequest,
    GovernanceRunResponse,
    LatestGovernanceResponse,
)
from app.services.github_client import GitHubClient
from app.services.governance_service import GovernanceService

router = APIRouter()


# -------------------------------------------------
# Trigger Governance Run
# POST /api/governance/run
# -------------------------------------------------
@router.post("/run", response_model=GovernanceRunResponse)
async def trigger_governance_run(
    payload: GovernanceRunRequest,
    gh: GitHubClient = Depends(),
    governance_service: GovernanceService = Depends()
):
    # 1. Create queued run record
    run = await governance_service.create_run(
        repo_id=payload.repo_id,
        mode=payload.mode
    )

    # 2. Trigger GitHub workflow_dispatch
    if payload.mode == "github":
        await gh.trigger_workflow_dispatch(
            repo_owner="sentinel-ops-suite",
            repo_name="sentinel-ops-suite",
            workflow_file="workflow-governance.yml",
            ref=payload.ref
        )

    # 3. Return metadata
    return GovernanceRunResponse(
        run_id=run.id,
        status=run.status,
        triggered_at=run.triggered_at
    )


# -------------------------------------------------
# Get Latest Governance Run
# GET /api/governance/latest?repo_id=#
# -------------------------------------------------
@router.get("/latest", response_model=LatestGovernanceResponse)
async def get_latest_governance_run(
    repo_id: int,
    governance_service: GovernanceService = Depends()
):
    run = await governance_service.get_latest_run(repo_id)

    if not run:
        raise HTTPException(
            status_code=404,
            detail="No governance runs found for this repository"
        )

    return LatestGovernanceResponse(
        run_id=run.id,
        repo_id=run.repo_id,
        status=run.status,
        score=run.score,
        violations_count=run.violations_count,
        triggered_at=run.triggered_at,
        completed_at=run.completed_at,
    )
