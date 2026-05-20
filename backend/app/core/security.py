# /home/ubuntu/sentinel-ops-suite/backend/app/core/security.py

import pyotp
from passlib.context import CryptContext
from sqlalchemy.orm import Session as DBSession

# IMPORTANT:
# Do NOT import User or session models at module import time.
# This avoids circular imports with app.models.* and app.db.base.

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------------------------------------------------------------------
# Password Hashing
# ---------------------------------------------------------------------------

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# ---------------------------------------------------------------------------
# TOTP MFA
# ---------------------------------------------------------------------------

def generate_mfa_secret() -> str:
    return pyotp.random_base32()


def get_totp(secret: str) -> pyotp.TOTP:
    return pyotp.TOTP(secret)


def verify_totp(secret: str, code: str) -> bool:
    totp = get_totp(secret)
    return totp.verify(code, valid_window=1)


# ---------------------------------------------------------------------------
# Session Validation Wrapper
# ---------------------------------------------------------------------------

def authenticate_session(db: DBSession, session_id: str):
    """
    Validate a session_id and return the associated user.
    Returns None if session is missing or expired.
    """
    from src.session_models import validate_session  # runtime import avoids circulars

    session = validate_session(db, session_id)
    if not session:
        return None

    return session.user


# ---------------------------------------------------------------------------
# Login Flow Helpers
# ---------------------------------------------------------------------------

def authenticate_user(db: DBSession, username: str, password: str):
    """
    Validate user credentials using USERNAME instead of email.
    Returns User if valid, None otherwise.
    """
    from app.models.user import User  # runtime import avoids circulars

    # Username-based lookup (correct for your login flow)
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    # Verify bcrypt password
    if not verify_password(password, user.password_hash):
        return None

    return user


def finalize_login(
    db: DBSession,
    user,
    ip_address: str | None,
    user_agent: str | None,
):
    """
    Enforce single active session, create a new session,
    and return the session object.
    """
    from src.session_models import (
        destroy_session,
        destroy_existing_sessions,
        create_session,
    )

    # Safety no-ops
    destroy_session(db, session_id=None)
    destroy_session(db, session_id="")

    # Enforce single active session
    destroy_existing_sessions(db, user.id)

    # Create new session
    session = create_session(
        db=db,
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return session
