"""Add avatar_version to users

Revision ID: 7807dda82440
Revises: 20260518_user_preferences
Create Date: 2026-05-18 00:00:00
"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = "7807dda82440"
down_revision = "20260518_user_preferences"
branch_labels = None
depends_on = None


def upgrade():
    # Add avatar_version with default=1
    op.add_column(
        "users",
        sa.Column("avatar_version", sa.Integer(), nullable=False, server_default="1")
    )


def downgrade():
    # Remove avatar_version
    op.drop_column("users", "avatar_version")
