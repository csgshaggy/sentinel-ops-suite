"""merge heads

Revision ID: 44b7f12db794
Revises: ecc6a8cdedfd, create_sessions_table
Create Date: 2026-05-28 23:30:50.542594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44b7f12db794'
down_revision: Union[str, None] = ('ecc6a8cdedfd', 'create_sessions_table')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
