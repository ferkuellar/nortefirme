from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.common.enums import ProjectStatus, VoltageType
from app.schemas.project_asset import ProjectAssetResponse
from app.schemas.sector import SectorResponse
from app.schemas.service import ServiceResponse


class ProjectBase(BaseModel):
    title: str = Field(..., max_length=200)
    slug: str | None = None
    short_description: str | None = Field(None, max_length=250)
    description: str | None = None
    client_name: str | None = None
    client_is_confidential: bool = False
    sector_id: int | None = None
    service_id: int | None = None
    voltage_type: VoltageType = VoltageType.NOT_APPLICABLE
    location_city: str | None = None
    location_state: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: ProjectStatus = ProjectStatus.PLANNED
    cover_image_url: str | None = None
    technical_scope: str | None = None
    deliverables: str | None = None
    challenges: str | None = None
    solution: str | None = None
    results: str | None = None
    seo_title: str | None = None
    seo_description: str | None = Field(None, max_length=160)
    seo_keywords: str | None = None

    @model_validator(mode="after")
    def validate_project_dates(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("start_date cannot be after end_date")
        return self

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: str | None = Field(None, max_length=200)
    slug: str | None = None
    short_description: str | None = Field(None, max_length=250)
    description: str | None = None
    client_name: str | None = None
    client_is_confidential: bool | None = None
    sector_id: int | None = None
    service_id: int | None = None
    voltage_type: VoltageType | None = None
    location_city: str | None = None
    location_state: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: ProjectStatus | None = None
    cover_image_url: str | None = None
    technical_scope: str | None = None
    deliverables: str | None = None
    challenges: str | None = None
    solution: str | None = None
    results: str | None = None
    seo_title: str | None = None
    seo_description: str | None = Field(None, max_length=160)
    seo_keywords: str | None = None

    @model_validator(mode="after")
    def validate_project_dates(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("start_date cannot be after end_date")
        return self

class ProjectResponse(ProjectBase):
    id: int
    is_featured: bool
    is_published: bool
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ProjectDetailResponse(ProjectResponse):
    sector: SectorResponse | None = None
    service: ServiceResponse | None = None
    assets: list[ProjectAssetResponse] = []
