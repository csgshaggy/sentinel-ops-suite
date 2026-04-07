# backend/app/core/security.py

from datetime import datetime, timedelta
import secrets
from passlib.context import CryptContext

# ---------------------------------------------------------------------------
# PASSWORD HASHING
# ---------------------------------------------------------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------------------------
# SESSION / TOKEN UTILITIES
# ---------------------------------------------------------------------------

def generate_session_token() -> str:
    """
    Generate a secure, opaque session token.
    Not a JWT — intentionally simple and safe.
    """
    return secrets.token_urlsafe(32)


def create_expiry(minutes: int = 60) -> datetime:
    """Return a UTC timestamp representing expiration time."""
    return datetime.utcnow() + timedelta(minutes=minutes)


def is_expired(expires_at: datetime) -> bool:
    """Check whether a timestamp has passed."""
    return datetime.utcnow() > expires_at
