# =====================================================================
# Legacy Authentication API (Deprecated)
# This module previously implemented JWT + cookie hybrid auth.
# It is now disabled in favor of the unified DB-backed session system
# located in: app/routers/auth.py
# =====================================================================

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def deprecated_login():
    raise HTTPException(
        status_code=400,
        detail="Legacy JWT/cookie login is disabled. Use /api/auth/login instead."
    )

@router.post("/logout")
def deprecated_logout():
    raise HTTPException(
        status_code=400,
        detail="Legacy logout is disabled. Use /api/auth/logout instead."
    )

@router.post("/create")
def deprecated_create():
    raise HTTPException(
        status_code=400,
        detail="Legacy user creation is disabled. Use /api/users/create instead."
    )

@router.get("/me")
def deprecated_me():
    raise HTTPException(
        status_code=400,
        detail="Legacy /me endpoint is disabled. Use /api/auth/session-info instead."
    )

@router.get("/validate")
def deprecated_validate():
    raise HTTPException(
        status_code=400,
        detail="Legacy session validation is disabled. Use /api/auth/session-info instead."
    )
