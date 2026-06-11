# /app/services/governance_service.py
# SentinelOps – Governance Service Layer

from sqlalchemy import select
from app.models.governance_run import GovernanceRun
from app.models.workflow_file import WorkflowFile
from app.db import async_session


class GovernanceService:

    # -------------------------------------------------
    # Create a new governance run (queued)
    # -------------------------------------------------
    async def create_run(self, repo_id: int, mode: str):
        async with async_session() as session:
            run = GovernanceRun(
                repo_id=repo_id,
                mode=mode,
                status="queued"
            )
            session.add(run)
            await session.commit()
            await session.refresh(run)
            return run

    # -------------------------------------------------
    # Fetch the latest governance run for a repository
    # -------------------------------------------------
    async def get_latest_run(self, repo_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(GovernanceRun)
                .where(GovernanceRun.repo_id == repo_id)
                .order_by(GovernanceRun.triggered_at.desc())
                .limit(1)
            )
            return result.scalar_one_or_none()

    # -------------------------------------------------
    # Fetch all workflow files for a repository
    # Used by: GET /api/governance/workflows
    # -------------------------------------------------
    async def get_workflows_for_repo(self, repo_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(WorkflowFile)
                .where(WorkflowFile.repo_id == repo_id)
                .order_by(WorkflowFile.path.asc())
            )
            return result.scalars().all()
