import enum
from datetime import UTC, date, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, Date, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Sector(str, enum.Enum):
    industrial = "industrial"
    commercial = "commercial"
    hospitality = "hospitality"
    healthcare = "healthcare"
    public_infrastructure = "public_infrastructure"
    residential = "residential"
    logistics = "logistics"
    corporate = "corporate"
    other = "other"


class ServiceType(str, enum.Enum):
    low_voltage_installation = "low_voltage_installation"
    medium_voltage_installation = "medium_voltage_installation"
    substation = "substation"
    transformer = "transformer"
    electrical_panels = "electrical_panels"
    grounding_system = "grounding_system"
    industrial_lighting = "industrial_lighting"
    preventive_maintenance = "preventive_maintenance"
    corrective_maintenance = "corrective_maintenance"
    electrical_diagnosis = "electrical_diagnosis"
    mixed_scope = "mixed_scope"


class VoltageType(str, enum.Enum):
    low_voltage = "low_voltage"
    medium_voltage = "medium_voltage"
    low_and_medium_voltage = "low_and_medium_voltage"
    not_applicable = "not_applicable"


class ProjectStatus(str, enum.Enum):
    planned = "planned"
    in_progress = "in_progress"
    completed = "completed"
    on_hold = "on_hold"
    cancelled = "cancelled"


class AssetType(str, enum.Enum):
    cover_image = "cover_image"
    gallery_image = "gallery_image"
    before_image = "before_image"
    after_image = "after_image"
    technical_document = "technical_document"
    delivery_evidence = "delivery_evidence"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(220), unique=True, nullable=False, index=True)
    short_description: Mapped[str | None] = mapped_column(String(250))
    description: Mapped[str | None] = mapped_column(Text)
    client_name: Mapped[str | None] = mapped_column(String(180))
    client_is_confidential: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sector: Mapped[Sector] = mapped_column(Enum(Sector, name="project_sector"), nullable=False)
    service_type: Mapped[ServiceType] = mapped_column(Enum(ServiceType, name="project_service_type"), nullable=False)
    voltage_type: Mapped[VoltageType] = mapped_column(Enum(VoltageType, name="project_voltage_type"), nullable=False)
    location_city: Mapped[str | None] = mapped_column(String(120))
    location_state: Mapped[str | None] = mapped_column(String(120))
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status"),
        default=ProjectStatus.planned,
        nullable=False,
        index=True,
    )
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    cover_image_url: Mapped[str | None] = mapped_column(String(700))
    gallery_images: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    technical_scope: Mapped[str | None] = mapped_column(Text)
    deliverables: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    challenges: Mapped[str | None] = mapped_column(Text)
    solution: Mapped[str | None] = mapped_column(Text)
    results: Mapped[str | None] = mapped_column(Text)
    seo_title: Mapped[str | None] = mapped_column(String(180))
    seo_description: Mapped[str | None] = mapped_column(String(160))
    seo_keywords: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    assets = relationship("ProjectAsset", back_populates="project", cascade="all, delete-orphan")


class ProjectAsset(Base):
    __tablename__ = "project_assets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True, nullable=False)
    asset_type: Mapped[AssetType] = mapped_column(Enum(AssetType, name="project_asset_type"), nullable=False)
    url: Mapped[str] = mapped_column(String(700), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(250))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    project = relationship("Project", back_populates="assets")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    action: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(80), nullable=False)
    details: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user = relationship("User", back_populates="audit_logs")
