import pyotp
from app.dependencies import get_current_user, get_db  # adjust to your project
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User

router = APIRouter(prefix="/mfa", tags=["mfa"])


# ---------- Schemas ----------


class MFAEnrollResponse(BaseModel):
    otpauth_url: str
    secret: str


class MFAVerifyRequest(BaseModel):
    code: str


class MFAStatusResponse(BaseModel):
    mfa_enabled: bool


# ---------- Helpers ----------


def _generate_mfa_secret() -> str:
    return pyotp.random_base32()


def _get_totp(secret: str) -> pyotp.TOTP:
    return pyotp.TOTP(
        s=secret,
        digits=settings.MFA_DIGITS,
        interval=settings.MFA_INTERVAL,
        issuer=settings.MFA_ISSUER,
    )


# ---------- Routes ----------


@router.get("/status", response_model=MFAStatusResponse)
def get_mfa_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return MFAStatusResponse(mfa_enabled=current_user.mfa_enabled)


@router.post("/enroll", response_model=MFAEnrollResponse)
def enroll_mfa(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Start MFA enrollment:
    - Generate secret if not present
    - Return otpauth URL + secret (frontend will turn into QR)
    """
    if current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA already enabled",
        )

    if not current_user.mfa_secret:
        current_user.mfa_secret = _generate_mfa_secret()
        db.add(current_user)
        db.commit()
        db.refresh(current_user)

    totp = _get_totp(current_user.mfa_secret)
    otpauth_url = totp.provisioning_uri(
        name=current_user.email,
        issuer_name=settings.MFA_ISSUER,
    )

    return MFAEnrollResponse(
        otpauth_url=otpauth_url,
        secret=current_user.mfa_secret,
    )


@router.post("/verify-enrollment", response_model=MFAStatusResponse)
def verify_enrollment_mfa(
    payload: MFAVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    User enters first code from authenticator app to confirm enrollment.
    """
    if not current_user.mfa_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA not in enrollment state",
        )

    totp = _get_totp(current_user.mfa_secret)
    if not totp.verify(payload.code, valid_window=1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid MFA code",
        )

    current_user.mfa_enabled = True
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return MFAStatusResponse(mfa_enabled=True)


@router.post("/disable", response_model=MFAStatusResponse)
def disable_mfa(
    payload: MFAVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Disable MFA after verifying a valid code.
    """
    if not current_user.mfa_enabled or not current_user.mfa_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA not enabled",
        )

    totp = _get_totp(current_user.mfa_secret)
    if not totp.verify(payload.code, valid_window=1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid MFA code",
        )

    current_user.mfa_enabled = False
    current_user.mfa_secret = None
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return MFAStatusResponse(mfa_enabled=False)
