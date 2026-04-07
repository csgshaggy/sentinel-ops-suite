# File: app/routes/auth.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.auth import UserLogin, TokenResponse
from app.services.auth_service import AuthService
from app.core.db import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return AuthService.login(
        db=db,
        username=payload.username,
        password=payload.password
    )
