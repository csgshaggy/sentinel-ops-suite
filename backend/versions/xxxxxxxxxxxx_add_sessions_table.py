from alembic import op
import sqlalchemy as sa

# Use the actual revision id Alembic generated
revision = "16514d35da2b_add_sessions_table.py"
down_revision = ""  # or None if this is first
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.String(128), unique=True, nullable=False),
        sa.Column("user_id", sa.Integer, nullable=False, index=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("last_activity", sa.DateTime, nullable=False),
        sa.Column("ip_address", sa.String(64), nullable=True),
        sa.Column("user_agent", sa.String(256), nullable=True),
    )
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"])


def downgrade():
    op.drop_table("sessions")
