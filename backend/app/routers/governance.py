# /app/routers/governance.py
# SentinelOps – Governance API Router

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.governance import (
    GovernanceRunRequest,
    GovernanceRunResponse,
    LatestGovernanceResponse,
    WorkflowStatus,
    GovernanceSnapshotResponse,
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
    run = await governance_service.create_run(
        repo_id=payload.repo_id,
        mode=payload.mode
    )

    if payload.mode == "github":
        await gh.trigger_workflow_dispatch(
            repo_owner="sentinel-ops-suite",
            repo_name="sentinel-ops-suite",
            workflow_file="workflow-governance.yml",
            ref=payload.ref
        )

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


# -------------------------------------------------
# List Workflow Integrity Status
# GET /api/governance/workflows?repo_id=#
# -------------------------------------------------
@router.get("/workflows", response_model=list[WorkflowStatus])
async def list_workflows(
    repo_id: int,
    governance_service: GovernanceService = Depends()
):
    workflows = await governance_service.get_workflows_for_repo(repo_id)

    return [
        WorkflowStatus(
            workflow_id=w.id,
            repo_id=w.repo_id,
            path=w.path,
            status=w.status,
            violations_count=w.violations_count,
            last_validated_at=w.last_validated_at,
        )
        for w in workflows
    ]


# -------------------------------------------------
# Governance Snapshot (violations + metadata)
# GET /api/governance/snapshot/{run_id}
# -------------------------------------------------
@router.get("/snapshot/{run_id}", response_model=GovernanceSnapshotResponse)
async def get_governance_snapshot(
    run_id: int,
    governance_service: GovernanceService = Depends()
):
    snapshot = await governance_service.get_snapshot(run_id)

    if not snapshot:
        raise HTTPException(
            status_code=404,
            detail="Snapshot not found for this run_id"
        )

    return snapshot
