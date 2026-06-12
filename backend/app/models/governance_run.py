# app/models/governance_run.py
# SentinelOps — Governance Run Model

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base_class import Base


class GovernanceRun(Base):
    """
    Represents a single governance evaluation run.
    Stores metadata about the run and summary results.
    """
    __tablename__ = "governance_runs"

    id = Column(Integer, primary_key=True, index=True)
    repo = Column(String(255), nullable=False)
    branch = Column(String(255), nullable=False)
    triggered_by = Column(String(255), nullable=False)

    status = Column(String(50), nullable=False, default="pending")
    summary = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
