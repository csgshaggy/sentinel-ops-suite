import pyotp
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth/mfa", tags=["mfa"])

# In production, store this in DB per-user
user_mfa_secrets = {}


class VerifyCode(BaseModel):
    code: str


@router.post("/enroll")
def enroll_mfa(user_id: int = 1):
    secret = pyotp.random_base32()
    user_mfa_secrets[user_id] = secret

    totp = pyotp.TOTP(secret)
    otpauth_url = totp.provisioning_uri(
        name=f"user{user_id}@ssrf-console",
        issuer_name="SSRF Command Console",
    )

    return {"secret": secret, "otpauth_url": otpauth_url}


@router.post("/verify-enrollment")
def verify_enrollment(payload: VerifyCode, user_id: int = 1):
    secret = user_mfa_secrets.get(user_id)
    if not secret:
        raise HTTPException(status_code=400, detail="MFA not initialized")

    totp = pyotp.TOTP(secret)

    if not totp.verify(payload.code):
        raise HTTPException(status_code=400, detail="Invalid code")

    return {"status": "verified"}
