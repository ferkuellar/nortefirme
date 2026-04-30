
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.common.enums import AssetType
from app.common.exceptions import NotFoundException
from app.core.permissions import require_editor, require_viewer
from app.db.session import get_db
from app.models.user import User
from app.repositories.project_asset_repository import ProjectAssetRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.project_asset import ProjectAssetResponse
from app.services.audit_service import AuditService
from app.services.upload_service import UploadService

router = APIRouter()
asset_repo = ProjectAssetRepository()
project_repo = ProjectRepository()

@router.post("/projects/{project_id}/assets", response_model=ProjectAssetResponse)
async def upload_asset(
    project_id: int,
    file: UploadFile = File(...),
    asset_type: AssetType = Form(...),
    description: str | None = Form(None),
    alt_text: str | None = Form(None),
    sort_order: int = Form(0),
    is_public: bool = Form(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_editor)
):
    project = project_repo.get(db, project_id)
    if not project:
        raise NotFoundException("Project not found")

    url, filename, size, mime_type = await UploadService.validate_and_save(file, asset_type)

    obj_in = {
        "asset_type": asset_type,
        "url": url,
        "filename": filename,
        "original_filename": file.filename,
        "mime_type": mime_type,
        "size_bytes": size,
        "description": description,
        "alt_text": alt_text,
        "sort_order": sort_order,
        "is_public": is_public
    }

    asset = asset_repo.create(db, project_id, obj_in)
    if asset_type == AssetType.COVER_IMAGE:
        project.cover_image_url = url
        db.add(project)
        db.commit()
    AuditService.log(db, "asset_uploaded", current_user.id, "asset", asset.id)
    return asset

@router.get("/projects/{project_id}/assets", response_model=list[ProjectAssetResponse])
def get_project_assets(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    if not project_repo.get(db, project_id):
        raise NotFoundException("Project not found")
    return asset_repo.get_by_project(db, project_id)

@router.delete("/projects/{project_id}/assets/{asset_id}", response_model=ProjectAssetResponse)
def delete_asset(
    project_id: int,
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_editor),
):
    asset = asset_repo.get(db, asset_id)
    if not asset or asset.project_id != project_id:
        raise NotFoundException()

    asset_repo.delete(db, asset)
    AuditService.log(db, "asset_deleted", current_user.id, "asset", asset.id)
    return asset
