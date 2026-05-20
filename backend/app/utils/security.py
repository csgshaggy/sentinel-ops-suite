# /home/ubuntu/sentinel-ops-suite/backend/app/utils/security.py
# SentinelOps — Security Utilities (Hashing + Verification)

import hashlib


# ---------------------------------------------------------
# Password Hashing (Active)
# ---------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Deterministic SHA-256 hashing.
    Replace with bcrypt/argon2 in production.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """
    Verifies a password against a stored SHA-256 hash.
    """
    return hash_password(password) == hashed


# ---------------------------------------------------------
# Legacy JWT Compatibility Layer
# ---------------------------------------------------------
# Your system no longer uses JWTs, but older modules still
# import these names. Defining them prevents ImportError and
# allows the backend to start normally.
# ---------------------------------------------------------

def create_access_token(*args, **kwargs) -> str:
    return ""


def create_refresh_token(*args, **kwargs) -> str:
    return ""


def verify_access_token(*args, **kwargs) -> bool:
    return False


def verify_refresh_token(*args, **kwargs) -> bool:
    return False


def decode_token(*args, **kwargs):
    return None


def encode_token(*args, **kwargs):
    return ""
