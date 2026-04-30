
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.exceptions import NotFoundException
from app.db.session import get_db
from app.repositories.sector_repository import SectorRepository
from app.schemas.sector import SectorResponse

router = APIRouter()
sector_repo = SectorRepository()

@router.get("", response_model=list[SectorResponse])
def get_public_sectors(db: Session = Depends(get_db)):
    return sector_repo.get_multi(db, skip=0, limit=100, active_only=True)

@router.get("/{slug}", response_model=SectorResponse)
def get_public_sector_by_slug(slug: str, db: Session = Depends(get_db)):
    sector = sector_repo.get_by_slug(db, slug)
    if not sector or not sector.is_active:
        raise NotFoundException("Sector not found")
    return sector
