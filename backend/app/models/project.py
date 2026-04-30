from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.common.enums import ProjectStatus, VoltageType
from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    short_description = Column(String(250), nullable=True)
    description = Column(Text, nullable=True)
    
    client_name = Column(String, nullable=True)
    client_is_confidential = Column(Boolean, default=False)
    
    sector_id = Column(Integer, ForeignKey("sectors.id"), nullable=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    
    voltage_type = Column(SQLEnum(VoltageType), default=VoltageType.NOT_APPLICABLE)
    location_city = Column(String, nullable=True)
    location_state = Column(String, nullable=True)
    
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.PLANNED, index=True)
    is_featured = Column(Boolean, default=False, index=True)
    is_published = Column(Boolean, default=False, index=True)
    
    cover_image_url = Column(String, nullable=True)
    
    technical_scope = Column(Text, nullable=True)
    deliverables = Column(Text, nullable=True)
    challenges = Column(Text, nullable=True)
    solution = Column(Text, nullable=True)
    results = Column(Text, nullable=True)
    
    seo_title = Column(String, nullable=True)
    seo_description = Column(String(160), nullable=True)
    seo_keywords = Column(String, nullable=True)
    
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True, index=True)

    sector = relationship("Sector")
    service = relationship("Service")
    assets = relationship("ProjectAsset", back_populates="project")
