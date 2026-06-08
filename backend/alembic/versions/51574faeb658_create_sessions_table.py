"""Create sessions table

Revision ID: create_sessions_table
Revises: 7807dda82440
Create Date: 2026-05-25
"""

from alembic import op
import sqlalchemy as sa

revision = "create_sessions_table"
down_revision = "7807dda82440"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "sessions",
        sa.Column("session_id", sa.String(255), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade():
    op.drop_table("sessions")
