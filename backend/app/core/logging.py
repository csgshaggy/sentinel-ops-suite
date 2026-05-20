# /backend/app/core/logging.py
import json
import logging
from datetime import datetime

logger = logging.getLogger("session")

def log_session_event(event: str, **data):
    payload = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "event": event,
        **data,
    }
    logger.info("[SESSION] %s", json.dumps(payload))
