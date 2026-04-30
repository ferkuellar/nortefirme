
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.enums import ProjectStatus, VoltageType
from app.common.exceptions import NotFoundException
from app.common.pagination import PaginatedResponse, paginate
from app.db.session import get_db
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectDetailResponse, ProjectResponse

router = APIRouter()
project_repo = ProjectRepository()

@router.get("", response_model=PaginatedResponse[ProjectResponse])
def get_public_projects(
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
    sector: int | None = None,
    service: int | None = None,
    voltage_type: VoltageType | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    items, total = project_repo.get_multi(
        db, skip=skip, limit=limit, public_only=True,
        sector_id=sector, service_id=service, voltage_type=voltage_type, search=search
    )
    return paginate(items, page, limit, total)

@router.get("/featured", response_model=PaginatedResponse[ProjectResponse])
def get_featured_projects(db: Session = Depends(get_db)):
    items, total = project_repo.get_multi(db, skip=0, limit=6, public_only=True, is_featured=True)
    return paginate(items, 1, 6, total)

@router.get("/{slug}", response_model=ProjectDetailResponse)
def get_public_project_by_slug(slug: str, db: Session = Depends(get_db)):
    project = project_repo.get_by_slug(db, slug)
    if not project or not project.is_published or project.status != ProjectStatus.COMPLETED:
        raise NotFoundException("Project not found")
    return project
