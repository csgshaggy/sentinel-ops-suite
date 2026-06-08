"""add notifications column to users

Revision ID: 9965e478d59c
Revises: 7fee7a81e1f3
Create Date: 2026-06-08 07:33:59.656454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9965e478d59c'
down_revision: Union[str, None] = '7fee7a81e1f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
