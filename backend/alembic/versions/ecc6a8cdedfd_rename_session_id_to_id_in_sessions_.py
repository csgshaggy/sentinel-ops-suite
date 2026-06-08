"""Rename session_id to id in sessions table

Revision ID: ecc6a8cdedfd
Revises: 547d76fa4ac1
Create Date: 2026-05-28

"""


from alembic import op
import sqlalchemy as sa


# Replace with your actual revision IDs
revision = 'ecc6a8cdedfd'
down_revision = '547d76fa4ac1'
branch_labels = None
depends_on = None


def upgrade():
    # MySQL cannot rename a primary key column directly without dropping constraints.
    # This sequence is safe and preserves data.

    with op.batch_alter_table("sessions") as batch_op:
        # Drop the existing PK
        batch_op.drop_constraint("PRIMARY", type_="primary")

        # Rename the column
        batch_op.alter_column(
            "session_id",
            new_column_name="id",
            existing_type=sa.String(length=255),
            existing_nullable=False
        )

        # Recreate the PK on the new column
        batch_op.create_primary_key("PRIMARY", ["id"])


def downgrade():
    # Reverse the operation
    with op.batch_alter_table("sessions") as batch_op:
        batch_op.drop_constraint("PRIMARY", type_="primary")

        batch_op.alter_column(
            "id",
            new_column_name="session_id",
            existing_type=sa.String(length=255),
            existing_nullable=False
        )

        batch_op.create_primary_key("PRIMARY", ["session_id"])
