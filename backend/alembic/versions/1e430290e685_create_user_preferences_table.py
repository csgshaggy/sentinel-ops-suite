"""create user_preferences table

Revision ID: 20260518_user_preferences
Revises: <PUT_PREVIOUS_REVISION_ID_HERE>
Create Date: 2026-05-18 12:00:00
"""

from alembic import op
import sqlalchemy as sa

revision = "20260518_user_preferences"
down_revision = "92a1eb6befc5"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "user_preferences",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True),

        sa.Column("theme", sa.String(length=50), nullable=True, server_default="system"),
        sa.Column("accent", sa.String(length=50), nullable=True, server_default="cyan"),

        sa.Column("timezone", sa.String(length=255), nullable=True, server_default="UTC"),
        sa.Column("language", sa.String(length=10), nullable=True, server_default="en"),

        sa.Column("login_alerts", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("security_warnings", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("product_updates", sa.Boolean(), nullable=False, server_default=sa.text("false")),

        sa.Column("session_timeout", sa.Integer(), nullable=False, server_default="15"),
    )

def downgrade():
    op.drop_table("user_preferences")
