# /home/ubuntu/sentinel-ops-suite/backend/app/db/base.py

from sqlalchemy.orm import declarative_base

# This file MUST remain clean.
# No model imports here — prevents circular imports.
Base = declarative_base()
