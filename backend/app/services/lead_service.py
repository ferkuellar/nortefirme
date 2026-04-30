
from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.repositories.lead_repository import LeadRepository
from app.schemas.lead import LeadCreate


class LeadService:
    def __init__(self, lead_repo: LeadRepository):
        self.lead_repo = lead_repo

    def process_new_lead(self, db: Session, req: LeadCreate, ip_address: str | None, user_agent: str | None) -> Lead:
        # Basic anti-spam
        if "http://" in req.message or "https://" in req.message:
             pass # could flag as spam, but let's just save for now
             
        lead = self.lead_repo.create(db, req, ip_address, user_agent)
        
        # Future: Trigger email or n8n webhook
        
        return lead
