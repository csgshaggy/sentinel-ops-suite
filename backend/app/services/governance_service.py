# app/services/governance_service.py
# SentinelOps — Governance Service (SYNC Version, Final)

from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.governance_run import GovernanceRun
from app.models.workflow_file import WorkflowFile
from app.models.governance_snapshot import GovernanceSnapshot


class GovernanceService:

    # -------------------------------------------------
    # Create a new governance run
    # -------------------------------------------------
    def create_run(self, repo_id: int, mode: str):
        with SessionLocal() as session:
            run = GovernanceRun(
                repo_id=repo_id,
                mode=mode,
                status="queued",
            )
            session.add(run)
            session.commit()
            session.refresh(run)
            return run

    # -------------------------------------------------
    # Update run status
    # -------------------------------------------------
    def update_run_status(self, run_id: int, status: str):
        with SessionLocal() as session:
            run = session.query(GovernanceRun).filter_by(id=run_id).first()
            if not run:
                return None
            run.status = status
            session.commit()
            session.refresh(run)
            return run

    # -------------------------------------------------
    # Get a single run
    # -------------------------------------------------
    def get_run(self, run_id: int):
        with SessionLocal() as session:
            return session.query(GovernanceRun).filter_by(id=run_id).first()

    # -------------------------------------------------
    # List runs for a repo
    # -------------------------------------------------
    def list_runs(self, repo_id: int):
        with SessionLocal() as session:
            return (
                session.query(GovernanceRun)
                .filter_by(repo_id=repo_id)
                .order_by(GovernanceRun.created_at.desc())
                .all()
            )

    # -------------------------------------------------
    # Delete a run
    # -------------------------------------------------
    def delete_run(self, run_id: int):
        with SessionLocal() as session:
            run = session.query(GovernanceRun).filter_by(id=run_id).first()
            if not run:
                return False
            session.delete(run)
            session.commit()
            return True

    # -------------------------------------------------
    # Get latest run for a repo
    # -------------------------------------------------
    def get_latest_run(self, repo_id: int):
        with SessionLocal() as session:
            stmt = (
                select(GovernanceRun)
                .where(GovernanceRun.repo_id == repo_id)
                .order_by(GovernanceRun.triggered_at.desc())
                .limit(1)
            )
            return session.execute(stmt).scalar_one_or_none()

    # -------------------------------------------------
    # List workflow files for a repo
    # -------------------------------------------------
    def get_workflows_for_repo(self, repo_id: int):
        with SessionLocal() as session:
            stmt = (
                select(WorkflowFile)
                .where(WorkflowFile.repo_id == repo_id)
                .order_by(WorkflowFile.path.asc())
            )
            return session.execute(stmt).scalars().all()

    # -------------------------------------------------
    # Get snapshot for a run
    # -------------------------------------------------
    def get_snapshot(self, run_id: int):
        with SessionLocal() as session:
            stmt = (
                select(GovernanceSnapshot)
                .where(GovernanceSnapshot.run_id == run_id)
                .limit(1)
            )
            return session.execute(stmt).scalar_one_or_none()

    # -------------------------------------------------
    # Get run history for a repo
    # -------------------------------------------------
    def get_history(self, repo_id: int):
        with SessionLocal() as session:
            stmt = (
                select(GovernanceRun)
                .where(GovernanceRun.repo_id == repo_id)
                .order_by(GovernanceRun.triggered_at.desc())
            )
            return session.execute(stmt).scalars().all()

    # -------------------------------------------------
    # Governance KPIs
    # -------------------------------------------------
    def get_kpis(self):
        with SessionLocal() as session:
            total_runs = session.query(GovernanceRun).count()
            completed_runs = (
                session.query(GovernanceRun)
                .filter(GovernanceRun.status == "completed")
                .count()
            )
            failed_runs = (
                session.query(GovernanceRun)
                .filter(GovernanceRun.status == "failed")
                .count()
            )

            return {
                "total_runs": total_runs,
                "completed_runs": completed_runs,
                "failed_runs": failed_runs,
            }
