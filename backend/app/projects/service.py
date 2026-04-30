import re
from typing import Any

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.auth.models import User
from app.common.exceptions import bad_request, not_found
from app.projects.models import AuditLog, Project, ProjectStatus, Sector, ServiceType, VoltageType
from app.projects.schemas import ProjectCreate, ProjectUpdate


def slugify(value: str) -> str:
    normalized = value.lower().strip()
    normalized = re.sub(r"[^a-z0-9áéíóúüñ]+", "-", normalized)
    replacements = str.maketrans("áéíóúüñ", "aeiouun")
    normalized = normalized.translate(replacements)
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    return normalized or "proyecto-electrico"


def ensure_unique_slug(db: Session, slug: str, project_id: int | None = None) -> None:
    query = select(Project.id).where(Project.slug == slug)
    if project_id:
        query = query.where(Project.id != project_id)
    if db.scalar(query):
        raise bad_request("El slug ya está registrado en otro proyecto.")


def log_action(
    db: Session,
    user: User | None,
    action: str,
    entity_type: str,
    entity_id: int | str,
    details: dict[str, Any] | None = None,
) -> None:
    db.add(
        AuditLog(
            user_id=user.id if user else None,
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id),
            details=details or {},
        )
    )


def apply_filters(
    query: Select[tuple[Project]],
    *,
    sector: Sector | None = None,
    service_type: ServiceType | None = None,
    voltage_type: VoltageType | None = None,
    status: ProjectStatus | None = None,
    is_featured: bool | None = None,
    search: str | None = None,
) -> Select[tuple[Project]]:
    if sector:
        query = query.where(Project.sector == sector)
    if service_type:
        query = query.where(Project.service_type == service_type)
    if voltage_type:
        query = query.where(Project.voltage_type == voltage_type)
    if status:
        query = query.where(Project.status == status)
    if is_featured is not None:
        query = query.where(Project.is_featured == is_featured)
    if search:
        like = f"%{search.strip()}%"
        query = query.where(
            or_(
                Project.title.ilike(like),
                Project.short_description.ilike(like),
                Project.description.ilike(like),
                Project.client_name.ilike(like),
                Project.technical_scope.ilike(like),
            )
        )
    return query


def list_projects(
    db: Session,
    *,
    page: int,
    limit: int,
    public_only: bool = False,
    featured_only: bool = False,
    sector: Sector | None = None,
    service_type: ServiceType | None = None,
    voltage_type: VoltageType | None = None,
    status: ProjectStatus | None = None,
    is_featured: bool | None = None,
    search: str | None = None,
) -> tuple[list[Project], int]:
    query = select(Project).options(selectinload(Project.assets))
    if public_only:
        query = query.where(Project.is_published.is_(True), Project.status == ProjectStatus.completed)
    if featured_only:
        query = query.where(Project.is_featured.is_(True))
    query = apply_filters(
        query,
        sector=sector,
        service_type=service_type,
        voltage_type=voltage_type,
        status=status,
        is_featured=is_featured,
        search=search,
    )
    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    items = db.scalars(query.order_by(Project.created_at.desc()).offset((page - 1) * limit).limit(limit)).all()
    return list(items), total


def get_project(db: Session, project_id: int) -> Project:
    project = db.scalar(select(Project).options(selectinload(Project.assets)).where(Project.id == project_id))
    if not project:
        raise not_found("Proyecto no encontrado.")
    return project


def get_public_project_by_slug(db: Session, slug: str) -> Project:
    project = db.scalar(
        select(Project).options(selectinload(Project.assets)).where(
            Project.slug == slug,
            Project.is_published.is_(True),
            Project.status == ProjectStatus.completed,
        )
    )
    if not project:
        raise not_found("Proyecto no encontrado.")
    return project


def create_project(db: Session, payload: ProjectCreate, user: User) -> Project:
    data = payload.model_dump()
    data["slug"] = data["slug"] or slugify(payload.title)
    ensure_unique_slug(db, data["slug"])
    project = Project(**data)
    db.add(project)
    db.flush()
    log_action(db, user, "project_created", "project", project.id, {"title": project.title})
    db.commit()
    db.refresh(project)
    return project


def update_project(db: Session, project_id: int, payload: ProjectUpdate, user: User) -> Project:
    project = get_project(db, project_id)
    data = payload.model_dump()
    data["slug"] = data["slug"] or slugify(payload.title)
    ensure_unique_slug(db, data["slug"], project_id=project.id)
    for key, value in data.items():
        setattr(project, key, value)
    log_action(db, user, "project_updated", "project", project.id, {"title": project.title})
    db.commit()
    db.refresh(project)
    return project


def set_project_flag(db: Session, project_id: int, user: User, *, field: str, value: bool, action: str) -> Project:
    project = get_project(db, project_id)
    if (
        field == "is_published"
        and value
        and (not project.title or not project.description or not project.cover_image_url)
    ):
        raise bad_request("El proyecto requiere title, description y cover_image_url para publicarse.")
    setattr(project, field, value)
    log_action(db, user, action, "project", project.id)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int, user: User) -> None:
    project = get_project(db, project_id)
    log_action(db, user, "project_deleted", "project", project.id, {"title": project.title})
    db.delete(project)
    db.commit()
