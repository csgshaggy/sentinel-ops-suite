# app/models/workflow_file.py
# SentinelOps — Workflow File Model

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base_class import Base


class WorkflowFile(Base):
    """
    Represents a GitHub workflow file discovered during a governance run.
    Stores filename, path, and raw YAML content for evaluation.
    """
    __tablename__ = "workflow_files"

    id = Column(Integer, primary_key=True, index=True)

    governance_run_id = Column(
        Integer,
        ForeignKey("governance_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    filename = Column(String(255), nullable=False)
    path = Column(String(500), nullable=False)

    content = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
