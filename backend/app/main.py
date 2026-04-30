from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.auth.routes import router as auth_router
from app.core.config import settings
from app.core.database import Base, engine
from app.projects import models as project_models
from app.projects.routes import admin_router as admin_projects_router
from app.projects.routes import public_router as public_projects_router
from app.uploads.routes import router as uploads_router

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    openapi_url=f"{settings.api_prefix}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

if settings.app_env == "development" and settings.database_url.startswith("sqlite"):
    _ = project_models
    Base.metadata.create_all(bind=engine)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if settings.app_env == "development":
        print(f"Unhandled error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(status_code=500, content={"detail": "No fue posible procesar la solicitud."})


@app.get("/health", tags=["health"])
def health():
    return {"ok": True, "service": settings.app_name}


app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(public_projects_router, prefix=settings.api_prefix)
app.include_router(admin_projects_router, prefix=settings.api_prefix)
app.include_router(uploads_router, prefix=settings.api_prefix)
