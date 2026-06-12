# app/models/workflow_violation.py
# SentinelOps — Workflow Violation Model

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base_class import Base


class WorkflowViolation(Base):
    """
    Represents a single governance violation discovered in a workflow file.
    Each violation links to a workflow file and the parent governance run.
    """
    __tablename__ = "workflow_violations"

    id = Column(Integer, primary_key=True, index=True)

    governance_run_id = Column(
        Integer,
        ForeignKey("governance_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    workflow_file_id = Column(
        Integer,
        ForeignKey("workflow_files.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    rule_id = Column(String(255), nullable=False)
    severity = Column(String(50), nullable=False, default="medium")
    message = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
