from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.routes import require_editor_or_admin
from app.core.database import get_db
from app.projects.models import AssetType
from app.projects.schemas import ProjectAssetCreate, ProjectAssetRead
from app.uploads.service import create_asset, delete_asset, list_assets

router = APIRouter(prefix="/admin/projects/{project_id}/assets", tags=["project assets"])


@router.post("", response_model=ProjectAssetRead, status_code=status.HTTP_201_CREATED)
async def upload_asset(
    project_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_editor_or_admin)],
    file: Annotated[UploadFile, File()],
    asset_type: Annotated[AssetType, Form()],
    description: Annotated[str | None, Form()] = None,
    sort_order: Annotated[int, Form(ge=0)] = 0,
):
    payload = ProjectAssetCreate(asset_type=asset_type, description=description, sort_order=sort_order)
    return await create_asset(db, project_id, payload, file, user)


@router.get("", response_model=list[ProjectAssetRead])
def get_assets(
    project_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(require_editor_or_admin)],
):
    return list_assets(db, project_id)


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_asset(
    project_id: int,
    asset_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_editor_or_admin)],
) -> Response:
    delete_asset(db, project_id, asset_id, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
