from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.enums import Role
from app.common.exceptions import BadRequestException
from app.core.config import settings
from app.core.permissions import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, Token
from app.schemas.common import MessageResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()
user_repo = UserRepository()
auth_service = AuthService(user_repo)

@router.post("/register", response_model=UserResponse)
def register(req: UserCreate, db: Session = Depends(get_db)):
    if not settings.ALLOW_ADMIN_REGISTRATION:
        raise BadRequestException("Registration is closed")
    if req.role != Role.ADMIN:
        raise BadRequestException("Initial registration only allows an admin user")
    if user_repo.has_admin(db):
        raise BadRequestException("An admin user already exists")
    if user_repo.get_by_email(db, req.email):
        raise BadRequestException("Email already registered")
    return user_repo.create(db, req)

@router.post("/login", response_model=Token)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.authenticate(db, req)

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout", response_model=MessageResponse)
def logout():
    return {"success": True, "message": "Logged out successfully"}
