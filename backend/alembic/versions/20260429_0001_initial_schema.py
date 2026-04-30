"""initial schema

Revision ID: 20260429_0001
Revises:
Create Date: 2026-04-29
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260429_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    user_role = sa.Enum("admin", "editor", name="user_role")
    project_sector = sa.Enum(
        "industrial",
        "commercial",
        "hospitality",
        "healthcare",
        "public_infrastructure",
        "residential",
        "logistics",
        "corporate",
        "other",
        name="project_sector",
    )
    project_service_type = sa.Enum(
        "low_voltage_installation",
        "medium_voltage_installation",
        "substation",
        "transformer",
        "electrical_panels",
        "grounding_system",
        "industrial_lighting",
        "preventive_maintenance",
        "corrective_maintenance",
        "electrical_diagnosis",
        "mixed_scope",
        name="project_service_type",
    )
    project_voltage_type = sa.Enum(
        "low_voltage",
        "medium_voltage",
        "low_and_medium_voltage",
        "not_applicable",
        name="project_voltage_type",
    )
    project_status = sa.Enum("planned", "in_progress", "completed", "on_hold", "cancelled", name="project_status")
    project_asset_type = sa.Enum(
        "cover_image",
        "gallery_image",
        "before_image",
        "after_image",
        "technical_document",
        "delivery_evidence",
        name="project_asset_type",
    )

    user_role.create(op.get_bind(), checkfirst=True)
    project_sector.create(op.get_bind(), checkfirst=True)
    project_service_type.create(op.get_bind(), checkfirst=True)
    project_voltage_type.create(op.get_bind(), checkfirst=True)
    project_status.create(op.get_bind(), checkfirst=True)
    project_asset_type.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=180), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("slug", sa.String(length=220), nullable=False),
        sa.Column("short_description", sa.String(length=250), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("client_name", sa.String(length=180), nullable=True),
        sa.Column("client_is_confidential", sa.Boolean(), nullable=False),
        sa.Column("sector", project_sector, nullable=False),
        sa.Column("service_type", project_service_type, nullable=False),
        sa.Column("voltage_type", project_voltage_type, nullable=False),
        sa.Column("location_city", sa.String(length=120), nullable=True),
        sa.Column("location_state", sa.String(length=120), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("status", project_status, nullable=False),
        sa.Column("is_featured", sa.Boolean(), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
        sa.Column("cover_image_url", sa.String(length=700), nullable=True),
        sa.Column("gallery_images", sa.JSON(), nullable=False),
        sa.Column("technical_scope", sa.Text(), nullable=True),
        sa.Column("deliverables", sa.JSON(), nullable=False),
        sa.Column("challenges", sa.Text(), nullable=True),
        sa.Column("solution", sa.Text(), nullable=True),
        sa.Column("results", sa.Text(), nullable=True),
        sa.Column("seo_title", sa.String(length=180), nullable=True),
        sa.Column("seo_description", sa.String(length=160), nullable=True),
        sa.Column("seo_keywords", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_projects_id"), "projects", ["id"], unique=False)
    op.create_index(op.f("ix_projects_is_featured"), "projects", ["is_featured"], unique=False)
    op.create_index(op.f("ix_projects_is_published"), "projects", ["is_published"], unique=False)
    op.create_index(op.f("ix_projects_slug"), "projects", ["slug"], unique=True)
    op.create_index(op.f("ix_projects_status"), "projects", ["status"], unique=False)
    op.create_index(op.f("ix_projects_title"), "projects", ["title"], unique=False)

    op.create_table(
        "project_assets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("asset_type", project_asset_type, nullable=False),
        sa.Column("url", sa.String(length=700), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=250), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
    )
    op.create_index(op.f("ix_project_assets_id"), "project_assets", ["id"], unique=False)
    op.create_index(op.f("ix_project_assets_project_id"), "project_assets", ["project_id"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("action", sa.String(length=80), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=False),
        sa.Column("entity_id", sa.String(length=80), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
    )
    op.create_index(op.f("ix_audit_logs_action"), "audit_logs", ["action"], unique=False)
    op.create_index(op.f("ix_audit_logs_user_id"), "audit_logs", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_audit_logs_user_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_action"), table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index(op.f("ix_project_assets_project_id"), table_name="project_assets")
    op.drop_index(op.f("ix_project_assets_id"), table_name="project_assets")
    op.drop_table("project_assets")
    op.drop_index(op.f("ix_projects_title"), table_name="projects")
    op.drop_index(op.f("ix_projects_status"), table_name="projects")
    op.drop_index(op.f("ix_projects_slug"), table_name="projects")
    op.drop_index(op.f("ix_projects_is_published"), table_name="projects")
    op.drop_index(op.f("ix_projects_is_featured"), table_name="projects")
    op.drop_index(op.f("ix_projects_id"), table_name="projects")
    op.drop_table("projects")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    for enum_name in [
        "project_asset_type",
        "project_status",
        "project_voltage_type",
        "project_service_type",
        "project_sector",
        "user_role",
    ]:
        sa.Enum(name=enum_name).drop(op.get_bind(), checkfirst=True)
