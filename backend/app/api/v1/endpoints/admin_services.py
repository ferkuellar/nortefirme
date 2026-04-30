
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.exceptions import NotFoundException
from app.core.permissions import require_admin, require_viewer
from app.db.session import get_db
from app.models.user import User
from app.repositories.service_repository import ServiceRepository
from app.schemas.service import ServiceCreate, ServiceResponse, ServiceUpdate
from app.services.audit_service import AuditService

router = APIRouter()
service_repo = ServiceRepository()

@router.get("", response_model=list[ServiceResponse])
def get_admin_services(db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    return service_repo.get_multi(db, skip=0, limit=100, active_only=False)

@router.post("", response_model=ServiceResponse)
def create_service(req: ServiceCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    service = service_repo.create(db, req)
    AuditService.log(db, "service_created", current_user.id, "service", service.id)
    return service

@router.get("/{id}", response_model=ServiceResponse)
def get_admin_service(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    service = service_repo.get(db, id)
    if not service:
        raise NotFoundException()
    return service

@router.put("/{id}", response_model=ServiceResponse)
def update_service(
    id: int,
    req: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    service = service_repo.get(db, id)
    if not service:
        raise NotFoundException()
    service = service_repo.update(db, service, req)
    AuditService.log(db, "service_updated", current_user.id, "service", service.id)
    return service

@router.delete("/{id}", response_model=ServiceResponse)
def delete_service(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    service = service_repo.get(db, id)
    if not service:
        raise NotFoundException()
    service_repo.delete(db, service)
    AuditService.log(db, "service_deleted", current_user.id, "service", id)
    return service
