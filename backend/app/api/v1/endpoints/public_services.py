
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.exceptions import NotFoundException
from app.db.session import get_db
from app.repositories.service_repository import ServiceRepository
from app.schemas.service import ServiceResponse

router = APIRouter()
service_repo = ServiceRepository()

@router.get("", response_model=list[ServiceResponse])
def get_public_services(db: Session = Depends(get_db)):
    return service_repo.get_multi(db, skip=0, limit=100, active_only=True)

@router.get("/{slug}", response_model=ServiceResponse)
def get_public_service_by_slug(slug: str, db: Session = Depends(get_db)):
    service = service_repo.get_by_slug(db, slug)
    if not service or not service.is_active:
        raise NotFoundException("Service not found")
    return service
