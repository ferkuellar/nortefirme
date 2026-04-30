
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.exceptions import NotFoundException
from app.core.permissions import require_admin, require_viewer
from app.db.session import get_db
from app.models.user import User
from app.repositories.sector_repository import SectorRepository
from app.schemas.sector import SectorCreate, SectorResponse, SectorUpdate
from app.services.audit_service import AuditService

router = APIRouter()
sector_repo = SectorRepository()

@router.get("", response_model=list[SectorResponse])
def get_admin_sectors(db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    return sector_repo.get_multi(db, skip=0, limit=100, active_only=False)

@router.post("", response_model=SectorResponse)
def create_sector(req: SectorCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    sector = sector_repo.create(db, req)
    AuditService.log(db, "sector_created", current_user.id, "sector", sector.id)
    return sector

@router.get("/{id}", response_model=SectorResponse)
def get_admin_sector(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    sector = sector_repo.get(db, id)
    if not sector:
        raise NotFoundException()
    return sector

@router.put("/{id}", response_model=SectorResponse)
def update_sector(
    id: int,
    req: SectorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    sector = sector_repo.get(db, id)
    if not sector:
        raise NotFoundException()
    sector = sector_repo.update(db, sector, req)
    AuditService.log(db, "sector_updated", current_user.id, "sector", sector.id)
    return sector

@router.delete("/{id}", response_model=SectorResponse)
def delete_sector(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    sector = sector_repo.get(db, id)
    if not sector:
        raise NotFoundException()
    sector_repo.delete(db, sector)
    AuditService.log(db, "sector_deleted", current_user.id, "sector", id)
    return sector
