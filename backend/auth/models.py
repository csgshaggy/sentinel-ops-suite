from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="viewer")  # admin, operator, viewer
    is_active = Column(Boolean, default=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    actor_email = Column(String, index=True, nullable=True)
    action = Column(String, nullable=False)          # e.g. "login", "user_create"
    target = Column(String, nullable=True)           # e.g. "user:alice@example.com"
    details = Column(Text, nullable=True)
