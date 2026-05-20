# /backend/app/core/mfa.py
import time
import pyotp
from uuid import uuid4

# In-memory store for pending login tokens
# Replace with Redis in production
PENDING_LOGIN = {}
PENDING_TTL = 180  # 3 minutes


def generate_pending_login_token():
    return uuid4().hex


def store_pending_login_token(user_id: int, token: str):
    PENDING_LOGIN[token] = {
        "user_id": user_id,
        "expires": time.time() + PENDING_TTL,
    }


def validate_pending_login_token(token: str):
    data = PENDING_LOGIN.get(token)
    if not data:
        return None

    if time.time() > data["expires"]:
        del PENDING_LOGIN[token]
        return None

    return data["user_id"]


def verify_totp_code(secret: str, code: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)
