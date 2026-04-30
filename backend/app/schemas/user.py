from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.common.enums import Role


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    role: Role = Role.VIEWER

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    role: Role | None = None
    password: str | None = Field(None, min_length=8)
    is_active: bool | None = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
