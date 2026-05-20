"""add sessions table

Revision ID: 16514d35da2b
Revises: 20260427_user_settings
Create Date: 2026-04-30 00:46:35.582016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16514d35da2b'
down_revision: Union[str, None] = '20260427_user_settings'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
