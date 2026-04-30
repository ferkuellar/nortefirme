from datetime import datetime

from sqlalchemy.orm import Session

from app.common.exceptions import UnauthorizedException
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, Token


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, db: Session, req: LoginRequest) -> Token:
        user = self.user_repo.get_by_email(db, req.email)
        if not user or not verify_password(req.password, user.hashed_password):
            raise UnauthorizedException(detail="Incorrect email or password")
        if not user.is_active:
            raise UnauthorizedException(detail="Inactive user")

        # Update last login
        user.last_login_at = datetime.utcnow()
        db.add(user)
        db.commit()

        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        return Token(access_token=access_token, refresh_token=refresh_token)
