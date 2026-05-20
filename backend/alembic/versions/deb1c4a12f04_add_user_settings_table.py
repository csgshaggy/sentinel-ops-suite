"""Add user_settings table

Revision ID: deb1c4a12f04
Revises:
Create Date: 2026-04-26 13:58:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'deb1c4a12f04'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_settings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('theme', sa.String(255), nullable=True),
        sa.Column('sidebar_collapsed', sa.Boolean(), nullable=True, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_user_settings_user_id'),
    )


def downgrade():
    op.drop_table('user_settings')
