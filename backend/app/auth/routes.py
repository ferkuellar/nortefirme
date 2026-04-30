import time
from collections import defaultdict, deque
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.models import User, UserRole
from app.auth.schemas import LoginRequest, TokenResponse, UserCreate, UserRead
from app.auth.service import authenticate_user, create_user, get_user_by_email, get_user_by_id, has_admin
from app.common.exceptions import forbidden
from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/auth/login")
login_attempts: dict[str, deque[float]] = defaultdict(deque)


def enforce_login_rate_limit(identifier: str) -> None:
    now = time.monotonic()
    window_seconds = 60
    max_attempts = 8
    attempts = login_attempts[identifier]

    while attempts and now - attempts[0] > window_seconds:
        attempts.popleft()

    if len(attempts) >= max_attempts:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiados intentos de login. Intenta de nuevo en un minuto.",
        )

    attempts.append(now)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if not payload or not payload.get("sub"):
        raise credentials_error

    user = get_user_by_id(db, int(payload["sub"]))
    if not user or not user.is_active:
        raise credentials_error
    return user


def require_admin(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role != UserRole.admin:
        raise forbidden("Solo un administrador puede realizar esta acción.")
    return current_user


def require_editor_or_admin(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role not in {UserRole.admin, UserRole.editor}:
        raise forbidden()
    return current_user


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_admin(payload: UserCreate, db: Annotated[Session, Depends(get_db)]) -> User:
    if not settings.allow_admin_registration:
        raise forbidden("El registro de administradores está desactivado.")

    if payload.role != UserRole.admin:
        raise forbidden("El registro público solo permite crear el administrador inicial.")

    if has_admin(db):
        raise forbidden("Ya existe un administrador registrado.")

    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El correo ya está registrado.")

    return create_user(db, payload)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Annotated[Session, Depends(get_db)]) -> TokenResponse:
    identifier = f'{request.client.host if request.client else "unknown"}:{payload.email.lower()}'
    enforce_login_rate_limit(identifier)

    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos.")

    token = create_access_token(str(user.id), {"role": user.role.value})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserRead)
def me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user
