# app/models/api_key.py
# SentinelOps — API Key Model

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)

    # Link to user
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="api_keys")

    # Human-readable name for the key
    name = Column(String(255), nullable=False)

    # SHA-256 hash of the API key (plaintext is never stored)
    key_hash = Column(String(255), nullable=False)

    # When the key was created
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Last time the key was used (optional)
    last_used = Column(DateTime(timezone=True), nullable=True)

    # Soft-revoke flag (service layer deletes, but this is future-proof)
    revoked = Column(Boolean, default=False, nullable=False)
