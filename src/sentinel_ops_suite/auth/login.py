import pyotp
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from sentinel_ops_suite.auth.mfa import user_mfa_secrets

router = APIRouter(prefix="/auth", tags=["auth"])

# Fake user for demo
FAKE_USER = {
    "id": 1,
    "username": "charlie",
    "password": "password123",  # replace with hashed password in real system
    "mfa_enabled": True,
}


class LoginRequest(BaseModel):
    username: str
    password: str


class MfaVerifyRequest(BaseModel):
    user_id: int
    code: str


@router.post("/login")
def login(payload: LoginRequest):
    # Validate username/password
    if (
        payload.username != FAKE_USER["username"]
        or payload.password != FAKE_USER["password"]
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # If MFA is enabled, require MFA challenge
    if FAKE_USER["mfa_enabled"]:
        return {"mfa_required": True, "user_id": FAKE_USER["id"]}

    # Otherwise return a session token (placeholder)
    return {"mfa_required": False, "token": "fake-session-token"}


@router.post("/login/mfa")
def login_mfa(payload: MfaVerifyRequest):
    secret = user_mfa_secrets.get(payload.user_id)
    if not secret:
        raise HTTPException(status_code=400, detail="MFA not configured")

    totp = pyotp.TOTP(secret)

    if not totp.verify(payload.code):
        raise HTTPException(status_code=400, detail="Invalid MFA code")

    return {"token": "fake-session-token"}
