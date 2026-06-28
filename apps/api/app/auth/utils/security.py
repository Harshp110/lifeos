from datetime import datetime, timedelta, UTC

from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def create_refresh_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        days=settings.refresh_token_expire_days
    )

    payload = {
        "sub": subject,
        "exp": expire,
        "type": "refresh",
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )