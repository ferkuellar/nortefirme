from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.projects.models import AssetType, ProjectStatus, Sector, ServiceType, VoltageType


def default_seo_title(title: str, city: str | None, state: str | None) -> str:
    location = ", ".join(part for part in [city, state] if part)
    return f'{title} | Norte Firme{f" en {location}" if location else ""}'[:180]


def default_seo_description(
    title: str, sector: Sector, service_type: ServiceType, city: str | None, state: str | None
) -> str:
    location = ", ".join(part for part in [city, state] if part)
    text = f'Proyecto de {service_type.value.replace("_", " ")} para sector {sector.value.replace("_", " ")}'
    if location:
        text += f" en {location}"
    text += f": {title}."
    return text[:160]


class ProjectBase(BaseModel):
    title: str = Field(min_length=3, max_length=180)
    slug: str | None = Field(default=None, max_length=220, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    short_description: str | None = Field(default=None, max_length=250)
    description: str | None = None
    client_name: str | None = Field(default=None, max_length=180)
    client_is_confidential: bool = False
    sector: Sector
    service_type: ServiceType
    voltage_type: VoltageType
    location_city: str | None = Field(default=None, max_length=120)
    location_state: str | None = Field(default=None, max_length=120)
    start_date: date | None = None
    end_date: date | None = None
    status: ProjectStatus = ProjectStatus.planned
    is_featured: bool = False
    is_published: bool = False
    cover_image_url: str | None = Field(default=None, max_length=700)
    gallery_images: list[str] = Field(default_factory=list)
    technical_scope: str | None = None
    deliverables: list[str] = Field(default_factory=list)
    challenges: str | None = None
    solution: str | None = None
    results: str | None = None
    seo_title: str | None = Field(default=None, max_length=180)
    seo_description: str | None = Field(default=None, max_length=160)
    seo_keywords: list[str] = Field(default_factory=list)

    @field_validator("gallery_images", "deliverables", "seo_keywords")
    @classmethod
    def clean_string_lists(cls, value: list[str]) -> list[str]:
        return [item.strip() for item in value if item and item.strip()]

    @model_validator(mode="after")
    def validate_project(self) -> "ProjectBase":
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("start_date no debe ser posterior a end_date.")

        if self.is_published and (not self.title or not self.description or not self.cover_image_url):
            raise ValueError("is_published solo puede ser true si title, description y cover_image_url existen.")

        if not self.seo_title:
            self.seo_title = default_seo_title(self.title, self.location_city, self.location_state)

        if not self.seo_description:
            self.seo_description = default_seo_description(
                self.title,
                self.sector,
                self.service_type,
                self.location_city,
                self.location_state,
            )

        if not self.seo_keywords:
            self.seo_keywords = [
                self.title,
                self.sector.value,
                self.service_type.value,
                self.voltage_type.value,
                *(part for part in [self.location_city, self.location_state] if part),
            ]

        return self


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectAssetCreate(BaseModel):
    asset_type: AssetType
    description: str | None = Field(default=None, max_length=250)
    sort_order: int = Field(default=0, ge=0)


class ProjectAssetRead(BaseModel):
    id: int
    project_id: int
    asset_type: AssetType
    url: str
    filename: str
    description: str | None
    sort_order: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectRead(ProjectBase):
    id: int
    slug: str
    assets: list[ProjectAssetRead] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectPublic(BaseModel):
    id: int
    title: str
    slug: str
    short_description: str | None
    description: str | None
    client_name: str | None
    client_is_confidential: bool
    sector: Sector
    service_type: ServiceType
    voltage_type: VoltageType
    location_city: str | None
    location_state: str | None
    status: ProjectStatus
    is_featured: bool
    cover_image_url: str | None
    gallery_images: list[str]
    assets: list[ProjectAssetRead] = Field(default_factory=list)
    technical_scope: str | None
    deliverables: list[str]
    challenges: str | None
    solution: str | None
    results: str | None
    seo_title: str | None
    seo_description: str | None
    seo_keywords: list[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def hide_confidential_client(self) -> "ProjectPublic":
        if self.client_is_confidential:
            self.client_name = "Cliente industrial confidencial"
        return self
