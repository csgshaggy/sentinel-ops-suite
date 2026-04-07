# File: app/repositories/user_repository.py

from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()
