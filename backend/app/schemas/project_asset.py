from datetime import datetime

from pydantic import BaseModel

from app.common.enums import AssetType


class ProjectAssetBase(BaseModel):
    asset_type: AssetType
    description: str | None = None
    alt_text: str | None = None
    sort_order: int = 0
    is_public: bool = True

class ProjectAssetUpdate(BaseModel):
    asset_type: AssetType | None = None
    description: str | None = None
    alt_text: str | None = None
    sort_order: int | None = None
    is_public: bool | None = None

class ProjectAssetResponse(ProjectAssetBase):
    id: int
    project_id: int
    url: str
    filename: str
    original_filename: str
    mime_type: str
    size_bytes: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
