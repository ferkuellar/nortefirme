from sqlalchemy import text
from sqlalchemy.engine import Engine


def _columns(engine: Engine, table_name: str) -> set[str]:
    with engine.connect() as connection:
        rows = connection.execute(text(f"PRAGMA table_info({table_name})")).mappings().all()
    return {row["name"] for row in rows}


def _add_column(engine: Engine, table_name: str, column_name: str, ddl: str) -> None:
    if column_name in _columns(engine, table_name):
        return
    with engine.begin() as connection:
        connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {ddl}"))


def ensure_sqlite_dev_schema(engine: Engine) -> None:
    """Non-destructive compatibility updates for the local development SQLite DB."""
    with engine.begin() as connection:
        existing_tables = {
            row["name"]
            for row in connection.execute(
                text("SELECT name FROM sqlite_master WHERE type='table'")
            ).mappings()
        }

    if "users" in existing_tables:
        _add_column(engine, "users", "last_login_at", "last_login_at DATETIME")

    if "projects" in existing_tables:
        _add_column(engine, "projects", "sector_id", "sector_id INTEGER")
        _add_column(engine, "projects", "service_id", "service_id INTEGER")
        _add_column(engine, "projects", "published_at", "published_at DATETIME")
        _add_column(engine, "projects", "deleted_at", "deleted_at DATETIME")

    if "project_assets" in existing_tables:
        _add_column(engine, "project_assets", "storage_key", "storage_key VARCHAR")
        _add_column(engine, "project_assets", "original_filename", "original_filename VARCHAR NOT NULL DEFAULT ''")
        _add_column(
            engine,
            "project_assets",
            "mime_type",
            "mime_type VARCHAR NOT NULL DEFAULT 'application/octet-stream'",
        )
        _add_column(engine, "project_assets", "size_bytes", "size_bytes INTEGER NOT NULL DEFAULT 0")
        _add_column(engine, "project_assets", "alt_text", "alt_text VARCHAR")
        _add_column(engine, "project_assets", "is_public", "is_public BOOLEAN NOT NULL DEFAULT 1")
        _add_column(engine, "project_assets", "updated_at", "updated_at DATETIME")
        _add_column(engine, "project_assets", "deleted_at", "deleted_at DATETIME")

    if "audit_logs" in existing_tables:
        _add_column(engine, "audit_logs", "ip_address", "ip_address VARCHAR")
        _add_column(engine, "audit_logs", "user_agent", "user_agent VARCHAR")
