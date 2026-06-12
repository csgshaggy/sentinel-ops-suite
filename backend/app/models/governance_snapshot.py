from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base


class GovernanceSnapshot(Base):
    __tablename__ = "governance_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("governance_runs.id"), nullable=False)
    repo_id = Column(Integer, nullable=False)

    violations_count = Column(Integer, default=0)
    details = Column(JSON, default={})  # renamed from metadata → details

    created_at = Column(DateTime(timezone=True), server_default=func.now())
