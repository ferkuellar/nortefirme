import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.db.sqlite_dev_migrations import ensure_sqlite_dev_schema

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend profesional para Norte Firme Infraestructura y Construcción",
    version="1.0.0",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
if settings.cors_origins_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Static files for local uploads
if settings.UPLOAD_BACKEND == "local":
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(api_router, prefix=settings.API_PREFIX)

if settings.APP_ENV == "development" and settings.DATABASE_URL.startswith("sqlite"):
    Base.metadata.create_all(bind=engine)
    ensure_sqlite_dev_schema(engine)
