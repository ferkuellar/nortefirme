
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.common.enums import LeadStatus
from app.common.exceptions import NotFoundException
from app.common.pagination import PaginatedResponse, paginate
from app.core.permissions import require_admin, require_editor, require_viewer
from app.db.session import get_db
from app.models.user import User
from app.repositories.lead_repository import LeadRepository
from app.schemas.common import MessageResponse
from app.schemas.lead import LeadCreate, LeadResponse, LeadUpdateStatus
from app.services.audit_service import AuditService
from app.services.lead_service import LeadService

router = APIRouter()
lead_repo = LeadRepository()
lead_service = LeadService(lead_repo)

@router.post("", response_model=MessageResponse)
def submit_lead(req: LeadCreate, request: Request, db: Session = Depends(get_db)):
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    lead_service.process_new_lead(db, req, ip_address, user_agent)
    return {"success": True, "message": "Solicitud recibida correctamente. Te contactaremos pronto."}

@router.get("/admin", response_model=PaginatedResponse[LeadResponse])
def get_admin_leads(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    status: LeadStatus | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_viewer)
):
    skip = (page - 1) * limit
    items, total = lead_repo.get_multi(db, skip=skip, limit=limit, status=status)
    return paginate(items, page, limit, total)

@router.get("/admin/{id}", response_model=LeadResponse)
def get_admin_lead(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    lead = lead_repo.get(db, id)
    if not lead:
        raise NotFoundException()
    return lead

@router.patch("/admin/{id}/status", response_model=LeadResponse)
def update_lead_status(
    id: int,
    req: LeadUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_editor),
):
    lead = lead_repo.get(db, id)
    if not lead:
        raise NotFoundException()
    lead = lead_repo.update_status(db, lead, req)
    AuditService.log(db, "lead_status_updated", current_user.id, "lead", lead.id)
    return lead

@router.delete("/admin/{id}", response_model=LeadResponse)
def delete_lead(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    lead = lead_repo.get(db, id)
    if not lead:
        raise NotFoundException()
    lead_repo.delete(db, lead)
    AuditService.log(db, "lead_deleted", current_user.id, "lead", id)
    return lead
