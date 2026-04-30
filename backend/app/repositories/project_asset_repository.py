
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.project_asset import ProjectAsset


class ProjectAssetRepository:
    def get(self, db: Session, id: int) -> ProjectAsset | None:
        return db.query(ProjectAsset).filter(ProjectAsset.id == id, ProjectAsset.deleted_at.is_(None)).first()

    def get_by_project(self, db: Session, project_id: int) -> list[ProjectAsset]:
        return db.query(ProjectAsset).filter(
            ProjectAsset.project_id == project_id,
            ProjectAsset.deleted_at.is_(None)
        ).order_by(ProjectAsset.sort_order.asc()).all()

    def create(self, db: Session, project_id: int, obj_in: dict) -> ProjectAsset:
        db_obj = ProjectAsset(project_id=project_id, **obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ProjectAsset) -> ProjectAsset:
        db_obj.deleted_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
