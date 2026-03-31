from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    # MFA-related
    mfa_enabled = Column(Boolean, nullable=False, default=False)
    mfa_secret = Column(String, nullable=True)  # base32 TOTP secret
