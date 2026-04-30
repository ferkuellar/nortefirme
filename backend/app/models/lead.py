from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy import Enum as SQLEnum

from app.common.enums import LeadStatus
from app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    company = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    project_type = Column(String, nullable=True)
    city = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    
    source = Column(String, default="website")
    status = Column(SQLEnum(LeadStatus), default=LeadStatus.NEW, index=True)
    
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
