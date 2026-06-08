"""add notifications column to users

Revision ID: 7fee7a81e1f3
Revises: 44b7f12db794
Create Date: 2026-06-08 07:33:35.778415
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7fee7a81e1f3"
down_revision: Union[str, None] = "44b7f12db794"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # MySQL does NOT allow defaults on JSON columns.
    op.add_column(
        "users",
        sa.Column(
            "notifications",
            sa.JSON(),
            nullable=True,
        ),
    )

    # Optional: backfill existing rows to avoid NULLs
    op.execute("UPDATE users SET notifications = '[]' WHERE notifications IS NULL")


def downgrade() -> None:
    op.drop_column("users", "notifications")
