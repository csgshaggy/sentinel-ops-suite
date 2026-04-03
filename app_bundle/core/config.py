from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Operator Console"
    MFA_ISSUER: str = "OperatorConsole"  # shows in authenticator app
    MFA_DIGITS: int = 6
    MFA_INTERVAL: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
