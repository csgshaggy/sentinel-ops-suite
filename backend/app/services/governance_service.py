from app.models.governance_run import GovernanceRun
from app.db import async_session

class GovernanceService:
    async def create_run(self, repo_id: int, mode: str):
        async with async_session() as session:
            run = GovernanceRun(repo_id=repo_id, mode=mode, status="queued")
            session.add(run)
            await session.commit()
            await session.refresh(run)
            return run
