# /home/ubuntu/sentinel-ops-suite/backend/app/repositories/user_repository.py

from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    """
    Repository for user-related database operations.
    """

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def create(db: Session, email: str, username: str, hashed_password: str) -> User:
        """
        Create a new user. Uses `hashed_password` to match the actual User model.
        """
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,   # <-- FIXED
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_last_login(db: Session, user: User) -> User:
        from datetime import datetime

        user.last_login_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_password(db: Session, user: User, new_hashed_password: str) -> User:
        """
        Optional helper for future password reset/change flows.
        """
        user.hashed_password = new_hashed_password
        db.commit()
        db.refresh(user)
        return user
