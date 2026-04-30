from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.common.enums import Role
from app.common.exceptions import ForbiddenException, UnauthorizedException
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException()
    except JWTError as exc:
        raise UnauthorizedException() from exc

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise UnauthorizedException()
    if not user.is_active:
        raise UnauthorizedException(detail="Inactive user")
    return user

def require_role(roles: list[Role]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in [role.value for role in roles]:
            raise ForbiddenException()
        return current_user
    return role_checker

require_admin = require_role([Role.ADMIN])
require_editor = require_role([Role.ADMIN, Role.EDITOR])
require_viewer = require_role([Role.ADMIN, Role.EDITOR, Role.VIEWER])
