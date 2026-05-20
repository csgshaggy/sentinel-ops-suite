# /home/ubuntu/sentinel-ops-suite/backend/app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# ------------------------------------------------------------
# SQLAlchemy Engine
# ------------------------------------------------------------
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# ------------------------------------------------------------
# Session Factory
# ------------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ------------------------------------------------------------
# FastAPI Dependency
# ------------------------------------------------------------
def get_db():
    """
    FastAPI dependency that yields a database session.
    Ensures the session is closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["SessionLocal", "get_db", "engine"]

