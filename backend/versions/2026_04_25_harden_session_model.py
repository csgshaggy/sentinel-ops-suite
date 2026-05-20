"""Harden session model: add device_fingerprint, index expires_at

Revision ID: harden_session_model_20240425
Revises: <PUT_PREVIOUS_REVISION_ID_HERE>
Create Date: 2026-04-25

"""

from alembic import op
import sqlalchemy as sa


# ---------------------------------------------------------------------
# Revision identifiers
# ---------------------------------------------------------------------
revision = "harden_session_model_20240425"
down_revision = "<PUT_PREVIOUS_REVISION_ID_HERE>"
branch_labels = None
depends_on = None


def upgrade():
    # Add device_fingerprint column
    op.add_column(
        "sessions",
        sa.Column(
            "device_fingerprint",
            sa.String(length=255),
            nullable=True,
            comment="Optional client-side fingerprint for device binding",
        ),
    )

    # Add index for expires_at (TTL enforcement)
    op.create_index(
        "ix_sessions_expires_at",
        "sessions",
        ["expires_at"],
        unique=False,
    )


def downgrade():
    # Drop index
    op.drop_index("ix_sessions_expires_at", table_name="sessions")

    # Drop device_fingerprint column
    op.drop_column("sessions", "device_fingerprint")
