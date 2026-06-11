# /app/routers/mfa.py
# SentinelOps — Unified MFA Router (Setup Endpoint)

import pyotp
from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.sessions import get_session_by_id
from app.models.user import User

router = APIRouter(prefix="/api/mfa", tags=["mfa"])


# ------------------------------------------------------------
# Helper — get authenticated user
# ------------------------------------------------------------
def get_authenticated_user(session_id: str | None, db: Session) -> User:
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = get_session_by_id(db, session_id)
    if not session or session.is_expired():
        raise HTTPException(status_code=401, detail="Session expired")

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ------------------------------------------------------------
# F2 — MFA Setup (Generate Secret + QR URI)
# ------------------------------------------------------------
@router.get("/setup")
async def mfa_setup(
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    """
    Step 1 of MFA enrollment:
    - Generate a new TOTP secret
    - Store it in the user's record
    - Return provisioning URI for QR code
    """

    user = get_authenticated_user(session_id, db)

    # Generate new secret
    secret = pyotp.random_base32()

    # Store secret
    user.mfa_secret = secret
    db.commit()

    # Build provisioning URI for Google Authenticator
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(
        name=user.username,
        issuer_name="SentinelOps"
    )

    return {
        "secret": secret,
        "provisioning_uri": provisioning_uri,
    }

# ------------------------------------------------------------
# F3 — Enable MFA (Verify TOTP)
# ------------------------------------------------------------
@router.post("/enable")
async def mfa_enable(
    code: str,
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    """
    Step 2 of MFA enrollment:
    - User enters a 6-digit TOTP code
    - Verify it against the stored secret
    - If valid → enable MFA
    """

    user = get_authenticated_user(session_id, db)

    if not user.mfa_secret:
        raise HTTPException(status_code=400, detail="MFA not initialized")

    totp = pyotp.TOTP(user.mfa_secret)

    if not totp.verify(code):
        raise HTTPException(status_code=400, detail="Invalid MFA code")

    user.mfa_enabled = True
    db.commit()

    return {"success": True}

# ------------------------------------------------------------
# F4 — Disable MFA
# ------------------------------------------------------------
@router.post("/disable")
async def mfa_disable(
    session_id: str | None = Cookie(None),
    db: Session = Depends(get_db),
):
    """
    Disable MFA for the authenticated user:
    - Clear mfa_secret
    - Set mfa_enabled = False
    """

    user = get_authenticated_user(session_id, db)

    user.mfa_enabled = False
    user.mfa_secret = None
    db.commit()

    return {"success": True}


# ------------------------------------------------------------
# F5 — Verify MFA during login (no session yet)
# ------------------------------------------------------------
@router.post("/verify")
async def mfa_verify(
    user_id: int,
    code: str,
    db: Session = Depends(get_db),
):
    """
    Step 2 of login when MFA is enabled:
    - User has already passed username/password
    - No session exists yet
    - Validate TOTP code
    """

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.mfa_enabled or not user.mfa_secret:
        raise HTTPException(status_code=400, detail="MFA not enabled")

    totp = pyotp.TOTP(user.mfa_secret)

    if not totp.verify(code):
        raise HTTPException(status_code=400, detail="Invalid MFA code")

    return {"success": True}
