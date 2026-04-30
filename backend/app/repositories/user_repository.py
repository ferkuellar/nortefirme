
from sqlalchemy.orm import Session

from app.common.enums import Role
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def get(self, db: Session, id: int) -> User | None:
        return db.query(User).filter(User.id == id).first()

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email.lower()).first()

    def has_admin(self, db: Session) -> bool:
        return db.query(User.id).filter(User.role == Role.ADMIN.value).first() is not None

    def create(self, db: Session, user_in: UserCreate) -> User:
        db_user = User(
            email=user_in.email.lower(),
            full_name=user_in.full_name,
            hashed_password=get_password_hash(user_in.password),
            role=user_in.role.value
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
