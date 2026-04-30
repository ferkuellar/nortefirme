from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.enums import ProjectStatus
from app.common.exceptions import BadRequestException, NotFoundException
from app.common.pagination import PaginatedResponse, paginate
from app.core.permissions import require_admin, require_editor, require_viewer
from app.db.session import get_db
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectDetailResponse, ProjectResponse, ProjectUpdate
from app.services.audit_service import AuditService

router = APIRouter()
project_repo = ProjectRepository()

@router.get("", response_model=PaginatedResponse[ProjectResponse])
def get_admin_projects(
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
    status: ProjectStatus | None = None,
    is_featured: bool | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_viewer)
):
    skip = (page - 1) * limit
    items, total = project_repo.get_multi(
        db,
        skip=skip,
        limit=limit,
        status=status,
        is_featured=is_featured,
        search=search,
    )
    return paginate(items, page, limit, total)

@router.post("", response_model=ProjectDetailResponse)
def create_project(
    req: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_editor)
):
    project = project_repo.create(db, req)
    AuditService.log(db, "project_created", current_user.id, "project", project.id)
    return project

@router.get("/{id}", response_model=ProjectDetailResponse)
def get_admin_project(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    project = project_repo.get(db, id)
    if not project:
        raise NotFoundException()
    return project

@router.put("/{id}", response_model=ProjectDetailResponse)
def update_project(
    id: int,
    req: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_editor)
):
    project = project_repo.get(db, id)
    if not project:
        raise NotFoundException()
    project = project_repo.update(db, project, req)
    AuditService.log(db, "project_updated", current_user.id, "project", project.id)
    return project

@router.patch("/{id}/publish", response_model=ProjectDetailResponse)
def publish_project(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    project = project_repo.get(db, id)
    if not project:
        raise NotFoundException()
    if not all([project.title, project.description, project.short_description, project.cover_image_url]):
         raise BadRequestException("Project is missing required fields for publishing")
    project.is_published = True
    project.published_at = datetime.utcnow()
    db.commit()
    AuditService.log(db, "project_published", current_user.id, "project", project.id)
    return project

@router.patch("/{id}/unpublish", response_model=ProjectDetailResponse)
def unpublish_project(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    project = project_repo.get(db, id)
    if not project:
        raise NotFoundException()
    project.is_published = False
    project.is_featured = False
    db.commit()
    AuditService.log(db, "project_unpublished", current_user.id, "project", project.id)
    return project

@router.patch("/{id}/feature", response_model=ProjectDetailResponse)
def feature_project(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    project = project_repo.get(db, id)
    if not project:
        raise NotFoundException()
    if not project.is_published:
        raise BadRequestException("Cannot feature an unpublished project")
    project.is_featured = True
    db.commit()
    AuditService.log(db, "project_featured", current_user.id, "project", project.id)
    return project

@router.patch("/{id}/unfeature", response_model=ProjectDetailResponse)
def unfeature_project(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    project = project_repo.get(db, id)
    if not project:
        raise NotFoundException()
    project.is_featured = False
    db.commit()
    AuditService.log(db, "project_unfeatured", current_user.id, "project", project.id)
    return project

@router.delete("/{id}", response_model=ProjectDetailResponse)
def delete_project(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    project = project_repo.get(db, id)
    if not project:
        raise NotFoundException()
    project = project_repo.soft_delete(db, project)
    AuditService.log(db, "project_deleted", current_user.id, "project", project.id)
    return project
