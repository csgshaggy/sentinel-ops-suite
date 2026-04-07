from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# ---------------------------------------------------------------------------
# DATABASE URL (Your RDS MySQL instance)
# ---------------------------------------------------------------------------

DATABASE_URL = (
    "mysql+pymysql://admin:WlIZj7oECiyW20Uf9Y4P@"
    "sentinelcybercop.ce9u88wwevvx.us-east-1.rds.amazonaws.com/sentinelops"
)

# ---------------------------------------------------------------------------
# SQLALCHEMY ENGINE + SESSION
# ---------------------------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

# ---------------------------------------------------------------------------
# DB DEPENDENCY
# ---------------------------------------------------------------------------

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------------------------
# INIT DB
# ---------------------------------------------------------------------------

def init_db() -> None:
    """
    Import models and create tables if they do not exist.
    """
    try:
        from app import models  # noqa: F401
    except ImportError:
        pass

    Base.metadata.create_all(bind=engine)
