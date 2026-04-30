from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.common.enums import LeadStatus


class LeadBase(BaseModel):
    full_name: str = Field(..., max_length=150)
    company: str | None = Field(None, max_length=150)
    phone: str = Field(..., max_length=50)
    email: EmailStr | None = None
    project_type: str | None = Field(None, max_length=150)
    city: str | None = Field(None, max_length=100)
    message: str = Field(..., max_length=1000)

class LeadCreate(LeadBase):
    pass

class LeadUpdateStatus(BaseModel):
    status: LeadStatus

class LeadResponse(LeadBase):
    id: int
    source: str
    status: LeadStatus
    ip_address: str | None = None
    user_agent: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
