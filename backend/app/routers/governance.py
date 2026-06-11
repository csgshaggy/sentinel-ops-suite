from fastapi import APIRouter, Depends
from app.schemas.governance import GovernanceRunRequest, GovernanceRunResponse
from app.services.github_client import GitHubClient
from app.services.governance_service import GovernanceService

router = APIRouter()

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
