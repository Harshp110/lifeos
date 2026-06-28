from sqlalchemy.orm import Session

from app.auth.schemas.auth import LoginRequest, RegisterRequest
from app.auth.utils.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User


def register_user(db: Session, data: RegisterRequest) -> User:
    existing = db.query(User).filter(User.email == data.email).first()

    if existing:
        raise ValueError("Email already registered")

    user = User(
        full_name=data.full_name,
        email=data.email,
        hashed_password=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(db: Session, data: LoginRequest) -> tuple[str, str]:
    user = db.query(User).filter(User.email == data.email).first()

    if user is None:
        raise ValueError("Invalid email or password")

    if not verify_password(data.password, user.hashed_password):
        raise ValueError("Invalid email or password")

    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))

    return access, refresh
