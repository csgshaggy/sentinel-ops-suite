from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db import Base

class GovernanceRun(Base):
    __tablename__ = "governance_runs"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    mode = Column(String, nullable=False)
    status = Column(String, default="queued")
    triggered_at = Column(DateTime(timezone=True), server_default=func.now())
