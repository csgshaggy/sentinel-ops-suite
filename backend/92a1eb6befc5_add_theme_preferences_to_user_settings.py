"""add theme preferences to user_settings

Revision ID: 20260515_theme_prefs
Revises: <YOUR_PREVIOUS_REVISION>
Create Date: 2026-05-15 00:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "20260515_theme_prefs"
down_revision = "<YOUR_PREVIOUS_REVISION>"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user_settings",
        sa.Column("theme_mode", sa.String(), server_default="system")
    )
    op.add_column(
        "user_settings",
        sa.Column("accent_color", sa.String(), server_default="#4f46e5")
    )


def downgrade():
    op.drop_column("user_settings", "theme_mode")
    op.drop_column("user_settings", "accent_color")
