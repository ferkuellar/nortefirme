
from slugify import slugify
from sqlalchemy.orm import Session

from app.models.sector import Sector
from app.schemas.sector import SectorCreate, SectorUpdate


class SectorRepository:
    def get(self, db: Session, id: int) -> Sector | None:
        return db.query(Sector).filter(Sector.id == id).first()

    def get_by_slug(self, db: Session, slug: str) -> Sector | None:
        return db.query(Sector).filter(Sector.slug == slug).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100, active_only: bool = False) -> list[Sector]:
        query = db.query(Sector)
        if active_only:
            query = query.filter(Sector.is_active.is_(True))
        return query.order_by(Sector.sort_order.asc(), Sector.created_at.desc()).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: SectorCreate) -> Sector:
        slug = obj_in.slug or slugify(obj_in.name)
        db_obj = Sector(**obj_in.model_dump(exclude={"slug"}), slug=slug)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Sector, obj_in: SectorUpdate) -> Sector:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "name" in update_data and not update_data.get("slug"):
            update_data["slug"] = slugify(update_data["name"])
            
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Sector) -> Sector:
        db.delete(db_obj)
        db.commit()
        return db_obj
