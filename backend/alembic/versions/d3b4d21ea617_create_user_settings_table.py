"""create user_settings table

Revision ID: 20260427_user_settings
Revises: 547d76fa4ac1
Create Date: 2026-04-27 19:15:00
"""

from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision = "20260427_user_settings"
down_revision = "547d76fa4ac1"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_settings",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), unique=True),

        sa.Column("display_name", sa.String(length=255), nullable=True, server_default=""),
        sa.Column("landing_page", sa.String(length=255), nullable=True, server_default="dashboard"),

        sa.Column("show_profile", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("show_clock", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("use_24h", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("show_seconds", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("show_day", sa.Boolean(), nullable=False, server_default=sa.text("0")),

        sa.Column("sidebar_collapsed", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("enable_sounds", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("enable_toasts", sa.Boolean(), nullable=False, server_default=sa.text("1")),

        sa.Column("auto_refresh", sa.Integer(), nullable=False, server_default="0"),

        sa.Column("timezone", sa.String(length=255), nullable=True, server_default="UTC"),
        sa.Column("locale", sa.String(length=255), nullable=True, server_default="en-US"),
        sa.Column("time_format", sa.String(length=50), nullable=True, server_default="24h"),

        sa.Column("session_timeout", sa.Integer(), nullable=False, server_default="900"),
        sa.Column("auto_logout", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("reauth_sensitive", sa.Boolean(), nullable=False, server_default=sa.text("1")),
    )


def downgrade():
    op.drop_table("user_settings")
