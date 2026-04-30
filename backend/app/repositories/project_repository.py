from datetime import datetime

from slugify import slugify
from sqlalchemy import or_
from sqlalchemy.orm import Session, selectinload

from app.common.enums import ProjectStatus
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def get(self, db: Session, id: int) -> Project | None:
        return (
            db.query(Project)
            .options(selectinload(Project.assets), selectinload(Project.sector), selectinload(Project.service))
            .filter(Project.id == id, Project.deleted_at.is_(None))
            .first()
        )

    def get_by_slug(self, db: Session, slug: str) -> Project | None:
        return (
            db.query(Project)
            .options(selectinload(Project.assets), selectinload(Project.sector), selectinload(Project.service))
            .filter(Project.slug == slug, Project.deleted_at.is_(None))
            .first()
        )

    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 12,
        public_only: bool = False,
        **filters,
    ) -> tuple[list[Project], int]:
        query = (
            db.query(Project)
            .options(selectinload(Project.assets), selectinload(Project.sector), selectinload(Project.service))
            .filter(Project.deleted_at.is_(None))
        )

        if public_only:
            query = query.filter(Project.is_published.is_(True), Project.status == ProjectStatus.COMPLETED)
        if filters.get("status"):
            query = query.filter(Project.status == filters["status"])
        if filters.get("is_featured") is not None:
            query = query.filter(Project.is_featured.is_(filters["is_featured"]))
        if filters.get("sector_id"):
            query = query.filter(Project.sector_id == filters["sector_id"])
        if filters.get("service_id"):
            query = query.filter(Project.service_id == filters["service_id"])
        if filters.get("voltage_type"):
            query = query.filter(Project.voltage_type == filters["voltage_type"])
        if filters.get("search"):
            search = f"%{filters['search']}%"
            query = query.filter(
                or_(
                    Project.title.ilike(search),
                    Project.description.ilike(search),
                    Project.location_city.ilike(search)
                )
            )

        total = query.count()

        if public_only:
            query = query.order_by(Project.is_featured.desc(), Project.published_at.desc(), Project.created_at.desc())
        else:
            query = query.order_by(Project.created_at.desc())

        items = query.offset(skip).limit(limit).all()
        return items, total

    def create(self, db: Session, obj_in: ProjectCreate) -> Project:
        slug = obj_in.slug or slugify(obj_in.title)

        # Ensure slug uniqueness (simple implementation)
        existing = db.query(Project).filter(Project.slug == slug).first()
        if existing:
            slug = f"{slug}-{datetime.utcnow().strftime('%y%m%d%H%M%S')}"

        db_obj = Project(**obj_in.model_dump(exclude={"slug"}), slug=slug)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Project, obj_in: ProjectUpdate) -> Project:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "title" in update_data and not update_data.get("slug"):
            update_data["slug"] = slugify(update_data["title"])

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def soft_delete(self, db: Session, db_obj: Project) -> Project:
        db_obj.deleted_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        return db_obj
