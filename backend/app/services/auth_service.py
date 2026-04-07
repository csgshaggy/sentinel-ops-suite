# File: app/services/auth_service.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token, create_refresh_token
from app.repositories.user_repository import UserRepository

class AuthService:

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = UserRepository.get_by_username(db, username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        return user

    @staticmethod
    def login(db: Session, username: str, password: str):
        user = AuthService.authenticate_user(db, username, password)

        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})

        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role,
            }
        }
