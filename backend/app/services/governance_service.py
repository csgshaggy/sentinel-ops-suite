# /app/services/governance_service.py
# SentinelOps – Governance Service Layer

from sqlalchemy import select
from app.models.governance_run import GovernanceRun
from app.models.workflow_file import WorkflowFile
from app.models.workflow_violation import WorkflowViolation
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
    # -------------------------------------------------
    async def get_workflows_for_repo(self, repo_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(WorkflowFile)
                .where(WorkflowFile.repo_id == repo_id)
                .order_by(WorkflowFile.path.asc())
            )
            return result.scalars().all()

    # -------------------------------------------------
    # Governance Snapshot (violations + metadata)
    # -------------------------------------------------
    async def get_snapshot(self, run_id: int):
        async with async_session() as session:

            # 1. Fetch the run
            run_result = await session.execute(
                select(GovernanceRun).where(GovernanceRun.id == run_id)
            )
            run = run_result.scalar_one_or_none()
            if not run:
                return None

            # 2. Fetch workflows for this repo
            wf_result = await session.execute(
                select(WorkflowFile)
                .where(WorkflowFile.repo_id == run.repo_id)
                .order_by(WorkflowFile.path.asc())
            )
            workflows = wf_result.scalars().all()

            # 3. Fetch violations for all workflows
            violations_result = await session.execute(
                select(WorkflowViolation)
                .where(WorkflowViolation.run_id == run_id)
            )
            violations = violations_result.scalars().all()

            # 4. Group violations by workflow_id
            violations_by_workflow = {}
            for v in violations:
                violations_by_workflow.setdefault(v.workflow_id, []).append(v)

            # 5. Build snapshot structure
            snapshot = {
                "run_id": run.id,
                "repo_id": run.repo_id,
                "triggered_at": run.triggered_at,
                "completed_at": run.completed_at,
                "workflows": []
            }

            for wf in workflows:
                snapshot["workflows"].append({
                    "workflow_id": wf.id,
                    "path": wf.path,
                    "status": wf.status,
                    "violations": [
                        {
                            "rule_id": v.rule_id,
                            "message": v.message,
                            "severity": v.severity,
                            "file_path": v.file_path,
                            "line": v.line,
                            "auto_fixed": v.auto_fixed,
                        }
                        for v in violations_by_workflow.get(wf.id, [])
                    ]
                })

            return snapshot

    # -------------------------------------------------
    # Governance Run History (Route 5)
    # -------------------------------------------------
    async def get_history(self, repo_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(GovernanceRun)
                .where(GovernanceRun.repo_id == repo_id)
                .order_by(GovernanceRun.triggered_at.desc())
            )
            return result.scalars().all()

    # -------------------------------------------------
    # Governance KPIs (NEW)
    # -------------------------------------------------
    async def get_kpis(self):
        """
        Returns high-level governance KPIs for the dashboard.
        Replace with real SQL queries once KPI tables exist.
        """
        # Deterministic placeholder values
        return {
            "complianceCoverage": 92,
            "openActions": 14,
            "slaDrift": 3.2,
            "policyExceptions": 7,
        }
