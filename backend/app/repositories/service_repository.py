
from slugify import slugify
from sqlalchemy.orm import Session

from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate


class ServiceRepository:
    def get(self, db: Session, id: int) -> Service | None:
        return db.query(Service).filter(Service.id == id).first()

    def get_by_slug(self, db: Session, slug: str) -> Service | None:
        return db.query(Service).filter(Service.slug == slug).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100, active_only: bool = False) -> list[Service]:
        query = db.query(Service)
        if active_only:
            query = query.filter(Service.is_active.is_(True))
        return query.order_by(Service.sort_order.asc(), Service.created_at.desc()).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: ServiceCreate) -> Service:
        slug = obj_in.slug or slugify(obj_in.name)
        db_obj = Service(**obj_in.model_dump(exclude={"slug"}), slug=slug)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Service, obj_in: ServiceUpdate) -> Service:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "name" in update_data and not update_data.get("slug"):
            update_data["slug"] = slugify(update_data["name"])
            
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Service) -> Service:
        db.delete(db_obj)
        db.commit()
        return db_obj
