
from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdateStatus


class LeadRepository:
    def get(self, db: Session, id: int) -> Lead | None:
        return db.query(Lead).filter(Lead.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 50, **filters) -> tuple[list[Lead], int]:
        query = db.query(Lead)
        
        if filters.get("status"):
            query = query.filter(Lead.status == filters["status"])

        total = query.count()
        items = query.order_by(Lead.created_at.desc()).offset(skip).limit(limit).all()
        return items, total

    def create(
        self,
        db: Session,
        obj_in: LeadCreate,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> Lead:
        db_obj = Lead(
            **obj_in.model_dump(),
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_status(self, db: Session, db_obj: Lead, obj_in: LeadUpdateStatus) -> Lead:
        db_obj.status = obj_in.status
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Lead) -> Lead:
        db.delete(db_obj)
        db.commit()
        return db_obj
