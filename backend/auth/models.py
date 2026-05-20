from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# -------------------------------------------------
# USER MODEL (MATCHES REAL RDS TABLE)
# -------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)

    # SHA-256 password (used by login)
    hashed_password = Column(String(255), nullable=True)

    # bcrypt password (legacy)
    password_hash = Column(String(255), nullable=True)

    email = Column(String(255), unique=True, index=True, nullable=False)
    role = Column(String(50), nullable=True)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    # MFA
    mfa_enabled = Column(Boolean, nullable=False, default=False)
    mfa_secret = Column(String(255), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)

    session_token = Column(String(255), nullable=True)
    last_login = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)

    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")


# -------------------------------------------------
# AUDIT LOG MODEL
# -------------------------------------------------

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    actor_email = Column(String(255), index=True, nullable=True)
    action = Column(String(255), nullable=False)
    target = Column(String(255), nullable=True)
    details = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="audit_logs")


# -------------------------------------------------
# SESSION MODEL (MATCHES REAL RDS TABLE)
# -------------------------------------------------

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    session_id = Column(String(255), unique=True, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User", back_populates="sessions")

    created_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # ⭐ REQUIRED FIELD (fixes backend crash)
    is_active = Column(Boolean, nullable=False, default=True)

    last_activity_at = Column(DateTime, nullable=True)
    last_seen_at = Column(DateTime, nullable=True)

    user_agent = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    device_fingerprint = Column(String(255), nullable=True)
