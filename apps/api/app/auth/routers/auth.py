from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.auth.services.auth_service import (
    login_user,
    register_user,
)
from app.database.session import get_session

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=UserResponse)
def register(
    data: RegisterRequest,
    db: Annotated[Session, Depends(get_session)],
):
    try:
        user = register_user(db, data)
        return UserResponse.model_validate(user)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Annotated[Session, Depends(get_session)],
):
    try:
        access, refresh = login_user(db, data)

        return TokenResponse(
            access_token=access,
            refresh_token=refresh,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )

from app.auth.dependencies.current_user import get_current_user
from app.models.user import User


@router.get("/me", response_model=UserResponse)
def me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return UserResponse.model_validate(current_user)
