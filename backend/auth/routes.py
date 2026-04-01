# =====================================================================
# SSRF Command Console — Authentication API (Session Cookie Edition)
# =====================================================================

from backend.auth.audit import log_event
from backend.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.auth.models import User
from backend.auth.schemas import UserCreate, UserLogin, UserOut
from backend.auth.security import (
    SESSION_COOKIE_NAME,
    SESSION_EXPIRE_MINUTES,
    create_access_token,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


# ---------------------------------------------------------------------
# Login (Sets Secure HttpOnly Session Cookie)
# ---------------------------------------------------------------------
@router.post("/login")
def login(payload: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    # Set secure session cookie
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=SESSION_EXPIRE_MINUTES * 60,
        path="/",
    )

    log_event(
        db,
        actor_email=user.email,
        action="login",
        target=f"user:{user.email}",
        details="User logged in via session cookie",
    )

    return {"status": "ok"}


# ---------------------------------------------------------------------
# Logout (Clears Session Cookie)
# ---------------------------------------------------------------------
@router.post("/logout")
def logout(response: Response, user: User = Depends(get_current_user)):
    response.delete_cookie(SESSION_COOKIE_NAME)
    return {"status": "logged_out"}


# ---------------------------------------------------------------------
# Create User (Public or System Bootstrap)
# ---------------------------------------------------------------------
@router.post("/create", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(payload.password)
    user = User(email=payload.email, hashed_password=hashed, role=payload.role)
    db.add(user)
    db.commit()
    db.refresh(user)

    log_event(
        db,
        actor_email=None,
        action="user_self_create",
        target=f"user:{user.email}",
        details=f"Role={user.role}",
    )

    return user


# ---------------------------------------------------------------------
# Get Current User (Session Cookie Auth)
# ---------------------------------------------------------------------
@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
