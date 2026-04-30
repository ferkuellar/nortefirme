from datetime import datetime

from pydantic import BaseModel


class SectorBase(BaseModel):
    name: str
    slug: str | None = None
    description: str | None = None
    icon_name: str | None = None
    sort_order: int = 0
    is_active: bool = True

class SectorCreate(SectorBase):
    pass

class SectorUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    icon_name: str | None = None
    sort_order: int | None = None
    is_active: bool | None = None

class SectorResponse(SectorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
