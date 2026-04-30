import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.common.enums import ProjectStatus, Role, VoltageType
from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.project import Project
from app.models.sector import Sector
from app.models.service import Service
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    # 1. Admin User
    admin = db.query(User).filter(User.email == "admin@nortefirme.com.mx").first()
    if not admin:
        admin = User(
            email="admin@nortefirme.com.mx",
            full_name="Admin Demo",
            hashed_password=get_password_hash("ChangeMe123!"),
            role=Role.ADMIN.value
        )
        db.add(admin)
        logger.info("Admin user created")
    
    # 2. Services
    services = [
        {"name": "Instalaciones eléctricas en baja tensión", "slug": "instalaciones-baja-tension"},
        {"name": "Media tensión", "slug": "media-tension"},
        {"name": "Subestaciones eléctricas", "slug": "subestaciones"},
        {"name": "Transformadores", "slug": "transformadores"},
        {"name": "Tableros generales y derivados", "slug": "tableros"},
        {"name": "Canalizaciones eléctricas", "slug": "canalizaciones"},
        {"name": "Alumbrado industrial y comercial", "slug": "alumbrado"},
        {"name": "Sistemas de puesta a tierra", "slug": "puesta-tierra"},
        {"name": "Mantenimiento preventivo y correctivo", "slug": "mantenimiento"},
        {"name": "Diagnóstico y levantamientos", "slug": "diagnostico"},
        {"name": "Alimentadores eléctricos", "slug": "alimentadores"},
        {"name": "Obra eléctrica general", "slug": "obra-electrica"}
    ]
    
    for s in services:
        if not db.query(Service).filter(Service.slug == s["slug"]).first():
            db.add(Service(**s))
    
    # 3. Sectors
    sectors = [
        {"name": "Naves industriales", "slug": "naves-industriales"},
        {"name": "Comercios", "slug": "comercios"},
        {"name": "Edificios corporativos", "slug": "corporativos"},
        {"name": "Hoteles", "slug": "hoteles"},
        {"name": "Hospitales y clínicas", "slug": "hospitales"},
        {"name": "Desarrollos habitacionales", "slug": "habitacionales"},
        {"name": "Obra pública", "slug": "obra-publica"},
        {"name": "Parques industriales", "slug": "parques-industriales"},
        {"name": "Bodegas y centros logísticos", "slug": "bodegas"}
    ]
    
    for s in sectors:
        if not db.query(Sector).filter(Sector.slug == s["slug"]).first():
            db.add(Sector(**s))
            
    db.commit()

    # 4. Demo Projects
    projects = [
        {
            "title": "Instalación eléctrica en nave industrial",
            "slug": "instalacion-nave-industrial",
            "short_description": "Ejecución de canalizaciones, alimentadores, tableros y pruebas de continuidad.",
            "description": "Proyecto integral de electrificación para nave industrial de 5,000 m2.",
            "voltage_type": VoltageType.LOW_AND_MEDIUM_VOLTAGE,
            "location_city": "Chihuahua",
            "location_state": "Chihuahua",
            "status": ProjectStatus.COMPLETED,
            "is_published": True,
            "is_featured": True,
            "cover_image_url": "https://images.unsplash.com/photo-1581092921461-eab62e97a780?auto=format&fit=crop&w=800&q=80"
        },
        {
            "title": "Adecuación de tableros eléctricos comerciales",
            "slug": "tableros-comerciales",
            "short_description": "Reordenamiento e identificación de circuitos.",
            "description": "Mantenimiento y actualización normativa de tableros en centro comercial.",
            "voltage_type": VoltageType.LOW_VOLTAGE,
            "location_city": "Chihuahua",
            "location_state": "Chihuahua",
            "status": ProjectStatus.COMPLETED,
            "is_published": True,
            "is_featured": True,
            "cover_image_url": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=800&q=80"
        },
        {
            "title": "Mantenimiento preventivo de subestación",
            "slug": "mantenimiento-subestacion",
            "short_description": "Limpieza, reapriete y pruebas a transformador.",
            "description": "Mantenimiento programado a subestación tipo pedestal de 500 kVA.",
            "voltage_type": VoltageType.MEDIUM_VOLTAGE,
            "location_city": "Chihuahua",
            "location_state": "Chihuahua",
            "status": ProjectStatus.COMPLETED,
            "is_published": True,
            "is_featured": False,
            "cover_image_url": "https://images.unsplash.com/photo-1498084393753-b411b2d26b34?auto=format&fit=crop&w=800&q=80"
        },
        {
            "title": "Sistema de puesta a tierra para edificio corporativo",
            "slug": "puesta-tierra-corporativo",
            "short_description": "Instalación de red de tierras y medición.",
            "description": "Implementación de tierras físicas para SITE y pararrayos.",
            "voltage_type": VoltageType.LOW_VOLTAGE,
            "location_city": "Chihuahua",
            "location_state": "Chihuahua",
            "status": ProjectStatus.COMPLETED,
            "is_published": True,
            "is_featured": False,
            "cover_image_url": "https://images.unsplash.com/photo-1544724569-5f546fd6f2b6?auto=format&fit=crop&w=800&q=80"
        },
        {
            "title": "Alumbrado industrial en bodega logística",
            "slug": "alumbrado-logistica",
            "short_description": "Sustitución de luminarias por tecnología LED.",
            "description": "Proyecto de ahorro energético y mejora de iluminación en centro logístico.",
            "voltage_type": VoltageType.LOW_VOLTAGE,
            "location_city": "Chihuahua",
            "location_state": "Chihuahua",
            "status": ProjectStatus.COMPLETED,
            "is_published": True,
            "is_featured": True,
            "cover_image_url": "https://images.unsplash.com/photo-1565626424178-c8fc48560117?auto=format&fit=crop&w=800&q=80"
        }
    ]
    
    for p in projects:
        if not db.query(Project).filter(Project.slug == p["slug"]).first():
            p["published_at"] = datetime.utcnow()
            db.add(Project(**p))
    
    db.commit()
    logger.info("Seed data loaded successfully.")

def main() -> None:
    logger.info("Creating initial data")
    db = SessionLocal()
    init_db(db)
    db.close()
    logger.info("Initial data created")

if __name__ == "__main__":
    main()
