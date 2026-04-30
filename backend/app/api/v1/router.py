from fastapi import APIRouter

from app.api.v1.endpoints import (
    admin_projects,
    admin_sectors,
    admin_services,
    auth,
    health,
    leads,
    public_projects,
    public_sectors,
    public_services,
    uploads,
)

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(public_projects.router, prefix="/public/projects", tags=["Public Projects"])
api_router.include_router(public_services.router, prefix="/public/services", tags=["Public Services"])
api_router.include_router(public_sectors.router, prefix="/public/sectors", tags=["Public Sectors"])
api_router.include_router(leads.router, prefix="/leads", tags=["Leads"])
api_router.include_router(admin_projects.router, prefix="/admin/projects", tags=["Admin Projects"])
api_router.include_router(admin_services.router, prefix="/admin/services", tags=["Admin Services"])
api_router.include_router(admin_sectors.router, prefix="/admin/sectors", tags=["Admin Sectors"])
api_router.include_router(uploads.router, prefix="/admin", tags=["Uploads"])
