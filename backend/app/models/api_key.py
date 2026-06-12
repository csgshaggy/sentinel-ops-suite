# app/models/api_key.py
# SentinelOps — API Key Model (Aligned)

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="api_keys")

    name = Column(String(255), nullable=False)

    # Will store hashed API key (Step 4)
    key_hash = Column(String(255), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    last_used = Column(DateTime(timezone=True), nullable=True)

    revoked = Column(Boolean, default=False, nullable=False)
