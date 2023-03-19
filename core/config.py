import os
import secrets

from typing import Any, Dict, Optional
from pydantic import BaseSettings, validator, PostgresDsn

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = 'Test project for STARNAVI'
    SECRET_KEY: str = os.getenv("SECRET_KEY") if os.getenv("SECRET_KEY") else secrets.token_urlsafe(32)
    HOST: str = "localhost"
    PORT: str = "8000"
    # 60 minutes * 24 hours = 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    FIRST_SUPERUSER_EMAIL: str = os.getenv("FIRST_SUPERUSER_EMAIL")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")

    POSTGRES_SERVER: str = os.getenv("POSTGRES_USER")
    POSTGRES_USER: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URL: Optional[PostgresDsn] = None

    NUMBER_OF_USERS: int = int(os.getenv("NUMBER_OF_USERS"))
    MAX_POSTS_PER_USER: int = int(os.getenv("MAX_POSTS_PER_USER"))
    MAX_LIKES_PER_USER: int = int(os.getenv("MAX_LIKES_PER_USER"))

    @validator("SQLALCHEMY_DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True


settings = Settings()
