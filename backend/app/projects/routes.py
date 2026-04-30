from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.routes import require_editor_or_admin
from app.common.pagination import Page, build_page
from app.core.database import get_db
from app.projects.models import ProjectStatus, Sector, ServiceType, VoltageType
from app.projects.schemas import ProjectCreate, ProjectPublic, ProjectRead, ProjectUpdate
from app.projects.service import (
    create_project,
    delete_project,
    get_project,
    get_public_project_by_slug,
    list_projects,
    set_project_flag,
    update_project,
)

public_router = APIRouter(prefix="/public/projects", tags=["public projects"])
admin_router = APIRouter(prefix="/admin/projects", tags=["admin projects"])


@public_router.get("", response_model=Page[ProjectPublic])
def public_projects(
    db: Annotated[Session, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 12,
    sector: Sector | None = None,
    service_type: ServiceType | None = None,
    voltage_type: VoltageType | None = None,
    search: str | None = None,
) -> Page[ProjectPublic]:
    items, total = list_projects(
        db,
        page=page,
        limit=limit,
        public_only=True,
        sector=sector,
        service_type=service_type,
        voltage_type=voltage_type,
        search=search,
    )
    return build_page(items, total, page, limit)


@public_router.get("/featured", response_model=Page[ProjectPublic])
def featured_projects(
    db: Annotated[Session, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 12,
) -> Page[ProjectPublic]:
    items, total = list_projects(db, page=page, limit=limit, public_only=True, featured_only=True)
    return build_page(items, total, page, limit)


@public_router.get("/{slug}", response_model=ProjectPublic)
def public_project_detail(slug: str, db: Annotated[Session, Depends(get_db)]):
    return get_public_project_by_slug(db, slug)


@admin_router.get("", response_model=Page[ProjectRead])
def admin_projects(
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(require_editor_or_admin)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 12,
    sector: Sector | None = None,
    service_type: ServiceType | None = None,
    voltage_type: VoltageType | None = None,
    status: ProjectStatus | None = None,
    is_featured: bool | None = None,
    search: str | None = None,
) -> Page[ProjectRead]:
    items, total = list_projects(
        db,
        page=page,
        limit=limit,
        sector=sector,
        service_type=service_type,
        voltage_type=voltage_type,
        status=status,
        is_featured=is_featured,
        search=search,
    )
    return build_page(items, total, page, limit)


@admin_router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_admin_project(
    payload: ProjectCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_editor_or_admin)],
):
    return create_project(db, payload, user)


@admin_router.get("/{project_id}", response_model=ProjectRead)
def admin_project_detail(
    project_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(require_editor_or_admin)],
):
    return get_project(db, project_id)


@admin_router.put("/{project_id}", response_model=ProjectRead)
def update_admin_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_editor_or_admin)],
):
    return update_project(db, project_id, payload, user)


@admin_router.patch("/{project_id}/publish", response_model=ProjectRead)
def publish_project(
    project_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_editor_or_admin)],
):
    return set_project_flag(db, project_id, user, field="is_published", value=True, action="project_published")


@admin_router.patch("/{project_id}/unpublish", response_model=ProjectRead)
def unpublish_project(
    project_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_editor_or_admin)],
):
    return set_project_flag(db, project_id, user, field="is_published", value=False, action="project_unpublished")


@admin_router.patch("/{project_id}/feature", response_model=ProjectRead)
def feature_project(
    project_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_editor_or_admin)],
):
    return set_project_flag(db, project_id, user, field="is_featured", value=True, action="project_featured")


@admin_router.patch("/{project_id}/unfeature", response_model=ProjectRead)
def unfeature_project(
    project_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_editor_or_admin)],
):
    return set_project_flag(db, project_id, user, field="is_featured", value=False, action="project_unfeatured")


@admin_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin_project(
    project_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_editor_or_admin)],
) -> Response:
    delete_project(db, project_id, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
