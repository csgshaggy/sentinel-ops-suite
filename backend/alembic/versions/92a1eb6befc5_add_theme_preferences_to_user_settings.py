"""add theme preferences to user_settings

Revision ID: 92a1eb6befc5
Revises: 16514d35da2b
Create Date: 2026-05-16 12:06:10.015360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92a1eb6befc5'
down_revision: Union[str, None] = '16514d35da2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
