# app/services/governance_service.py
# SentinelOps — Governance Service (SYNC version)

from app.db.session import SessionLocal
from app.models.governance_run import GovernanceRun


class GovernanceService:
    def create_run(self, repo_id: int, mode: str):
        """
        Create a governance run entry (SYNC version).
        """
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

    def update_run_status(self, run_id: int, status: str):
        with SessionLocal() as session:
            run = session.query(GovernanceRun).filter_by(id=run_id).first()
            if not run:
                return None
            run.status = status
            session.commit()
            session.refresh(run)
            return run

    def get_run(self, run_id: int):
        with SessionLocal() as session:
            return session.query(GovernanceRun).filter_by(id=run_id).first()

    def list_runs(self, repo_id: int):
        with SessionLocal() as session:
            return (
                session.query(GovernanceRun)
                .filter_by(repo_id=repo_id)
                .order_by(GovernanceRun.created_at.desc())
                .all()
            )

    def delete_run(self, run_id: int):
        with SessionLocal() as session:
            run = session.query(GovernanceRun).filter_by(id=run_id).first()
            if not run:
                return False
            session.delete(run)
            session.commit()
            return True
