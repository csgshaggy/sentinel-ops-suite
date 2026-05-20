# /home/ubuntu/sentinel-ops-suite/backend/app/db/base.py
# SentinelOps — SQLAlchemy Base Model Registry

"""
This file ensures Alembic can discover all SQLAlchemy models.
Any new model must be imported here so migrations can detect it.
"""

# INVALID IMPORT REMOVED: app.database Base

# Import all models so Alembic can autogenerate migrations
from app.models.user import User
# INVALID IMPORT REMOVED: app.models.session Session
# INVALID IMPORT REMOVED: app.models.user_settings UserSettings

# If you add more models later, import them here.