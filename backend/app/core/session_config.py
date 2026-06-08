# /app/core/session_config.py
# SentinelOps — Session Configuration & Token Utilities

from datetime import timedelta
import secrets


# ---------------------------------------------------------
# Session Timing Configuration
# ---------------------------------------------------------

# Sliding inactivity timeout (minutes)
INACTIVITY_TIMEOUT_MINUTES = 15

# Absolute max lifetime (hours)
ABSOLUTE_SESSION_HOURS = 24


# ---------------------------------------------------------
# Cookie Configuration
# ---------------------------------------------------------

SESSION_COOKIE_NAME = "session_id"

COOKIE_SETTINGS = {
    "httponly": True,
    "secure": True,          # set False only for local dev
    "samesite": "strict",
    "path": "/",
}


# ---------------------------------------------------------
# Token Generator
# ---------------------------------------------------------

def generate_session_token() -> str:
    """
    Generate a cryptographically secure session token.
    32 bytes → 64 hex chars.
    """
    return secrets.token_hex(32)


# ---------------------------------------------------------
# TTL Helpers
# ---------------------------------------------------------

def inactivity_timedelta() -> timedelta:
    return timedelta(minutes=INACTIVITY_TIMEOUT_MINUTES)


def absolute_timedelta() -> timedelta:
    return timedelta(hours=ABSOLUTE_SESSION_HOURS)
