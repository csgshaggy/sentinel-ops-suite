# /home/ubuntu/sentinel-ops-suite/backend/app/auth/mfa.py
# SentinelOps — MFA / TOTP Verification (Pydantic v2, Sync, Deterministic)

import pyotp


def verify_totp(secret: str, code: str) -> bool:
    """
    Verifies a TOTP code using a deterministic secret.
    The secret is derived from the user's hashed_password[:16].

    This keeps MFA functional without requiring a full
    MFA enrollment flow yet.
    """
    try:
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)
    except Exception:
        return False
