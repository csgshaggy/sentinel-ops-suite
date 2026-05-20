# File: create_sessions_table.py
# One-time migration script to create the sessions table

from app.database import engine, Base
from src.session_models import Session  # noqa: F401  (import required for metadata)

print("Creating sessions table...")
Base.metadata.create_all(bind=engine)
print("Done.")
