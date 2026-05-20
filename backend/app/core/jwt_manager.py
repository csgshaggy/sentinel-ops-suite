# File: app/core/jwt_manager.py
# SentinelOps — JWT Session Management (HS256)

import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from os import getenv

JWT_SECRET = getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_session_token(user_id: int, role: str) -> str:
    """
    Create a signed JWT containing:
    - user_id
    - role
    - expiration timestamp
    """
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET is not set in environment.")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "user_id": user_id,
        "role": role,
        "exp": expire
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_session_token(token: str) -> dict:
    """
    Verify and decode a JWT.
    Returns the decoded payload if valid.
    Raises HTTPException if invalid or expired.
    """
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET is not set in environment.")

    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired.")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
