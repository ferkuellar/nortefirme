from sqlalchemy import select

from app.core.database import SessionLocal
from app.projects.models import Project, ProjectStatus, Sector, ServiceType, VoltageType
from app.projects.service import slugify

PROJECTS = [
    {
        "title": "Instalación eléctrica en nave industrial",
        "short_description": (
            "Infraestructura de baja tensión para nave industrial con tableros, alimentadores y canalización."
        ),
        "description": (
            "Ejecución de instalación eléctrica para nave industrial con enfoque en continuidad operativa, "
            "orden en canalizaciones y entrega técnica para mantenimiento."
        ),
        "client_name": "Cliente industrial confidencial",
        "client_is_confidential": True,
        "sector": Sector.industrial,
        "service_type": ServiceType.low_voltage_installation,
        "voltage_type": VoltageType.low_voltage,
        "location_city": "Chihuahua",
        "location_state": "Chihuahua",
        "status": ProjectStatus.completed,
        "is_featured": True,
        "is_published": True,
        "cover_image_url": "/uploads/demo/nave-industrial.webp",
        "gallery_images": ["/uploads/demo/nave-industrial-1.webp", "/uploads/demo/nave-industrial-2.webp"],
        "technical_scope": (
            "Suministro e instalación de alimentadores principales, tableros derivados, canalización EMT, "
            "sistema de puesta a tierra y adecuaciones eléctricas en baja tensión."
        ),
        "deliverables": [
            "Levantamiento técnico",
            "Instalación de canalización",
            "Montaje de tableros",
            "Pruebas de continuidad",
            "Memoria fotográfica",
            "Entrega técnica",
        ],
        "challenges": "Coordinar la ejecución eléctrica con trabajos simultáneos de obra civil y montaje de equipos.",
        "solution": (
            "Se definieron rutas eléctricas por etapas, ventanas de intervención y puntos de revisión con "
            "residente de obra."
        ),
        "results": (
            "Instalación ordenada, revisable y lista para operación con evidencia de avance y entrega documentada."
        ),
    },
    {
        "title": "Adecuación de tableros eléctricos comerciales",
        "short_description": "Corrección, identificación y balanceo de cargas en tableros para operación comercial.",
        "description": (
            "Adecuación de tableros generales y derivados en inmueble comercial para mejorar seguridad, "
            "orden y capacidad de mantenimiento."
        ),
        "client_name": "Plaza comercial regional",
        "client_is_confidential": True,
        "sector": Sector.commercial,
        "service_type": ServiceType.electrical_panels,
        "voltage_type": VoltageType.low_voltage,
        "location_city": "Chihuahua",
        "location_state": "Chihuahua",
        "status": ProjectStatus.completed,
        "is_featured": True,
        "is_published": True,
        "cover_image_url": "/uploads/demo/tableros-comerciales.webp",
        "gallery_images": ["/uploads/demo/tableros-comerciales-1.webp"],
        "technical_scope": (
            "Revisión de tableros, identificación de circuitos, reordenamiento de protecciones, "
            "balanceo de cargas y etiquetado."
        ),
        "deliverables": [
            "Diagnóstico eléctrico",
            "Identificación de circuitos",
            "Adecuación de tableros",
            "Reporte fotográfico",
        ],
        "challenges": "El inmueble requería mantener operación comercial durante las intervenciones.",
        "solution": (
            "Se trabajó por zonas y horarios controlados, priorizando circuitos críticos y minimizando "
            "interrupciones."
        ),
        "results": "Tableros más seguros, claros para operación y con mejor trazabilidad para mantenimiento.",
    },
    {
        "title": "Mantenimiento preventivo de subestación",
        "short_description": "Inspección y mantenimiento preventivo para subestación de media tensión.",
        "description": (
            "Servicio de mantenimiento preventivo enfocado en seguridad, continuidad operativa y revisión "
            "de componentes críticos de subestación."
        ),
        "client_name": "Cliente industrial confidencial",
        "client_is_confidential": True,
        "sector": Sector.industrial,
        "service_type": ServiceType.preventive_maintenance,
        "voltage_type": VoltageType.medium_voltage,
        "location_city": "Cuauhtémoc",
        "location_state": "Chihuahua",
        "status": ProjectStatus.completed,
        "is_featured": True,
        "is_published": True,
        "cover_image_url": "/uploads/demo/subestacion.webp",
        "gallery_images": ["/uploads/demo/subestacion-1.webp"],
        "technical_scope": (
            "Inspección visual, limpieza técnica, revisión de conexiones, verificación de protecciones "
            "y documentación de hallazgos."
        ),
        "deliverables": [
            "Plan de intervención",
            "Mantenimiento preventivo",
            "Registro de hallazgos",
            "Recomendaciones técnicas",
        ],
        "challenges": "La intervención debía realizarse con ventana limitada para evitar afectaciones operativas.",
        "solution": "Se preparó checklist técnico y secuencia de intervención para reducir tiempos fuera de servicio.",
        "results": "Subestación revisada, con hallazgos documentados y recomendaciones para continuidad operativa.",
    },
    {
        "title": "Sistema de puesta a tierra para edificio corporativo",
        "short_description": (
            "Implementación de sistema de puesta a tierra para protección eléctrica de edificio corporativo."
        ),
        "description": (
            "Diseño e instalación de sistema de puesta a tierra para proteger infraestructura eléctrica, "
            "tableros y equipos sensibles."
        ),
        "client_name": "Corporativo privado",
        "client_is_confidential": True,
        "sector": Sector.corporate,
        "service_type": ServiceType.grounding_system,
        "voltage_type": VoltageType.low_voltage,
        "location_city": "Chihuahua",
        "location_state": "Chihuahua",
        "status": ProjectStatus.completed,
        "is_featured": False,
        "is_published": True,
        "cover_image_url": "/uploads/demo/puesta-tierra.webp",
        "gallery_images": ["/uploads/demo/puesta-tierra-1.webp"],
        "technical_scope": (
            "Instalación de electrodos, conexiones, registros, unión equipotencial y revisión de continuidad."
        ),
        "deliverables": ["Levantamiento", "Instalación física", "Pruebas de continuidad", "Entrega de evidencia"],
        "challenges": "Integrar el sistema a una instalación existente con operación activa.",
        "solution": "Se seleccionaron rutas y puntos de conexión con mínima interferencia para usuarios del edificio.",
        "results": "Sistema instalado y documentado para mejorar seguridad eléctrica y protección de equipos.",
    },
    {
        "title": "Alumbrado industrial en bodega logística",
        "short_description": (
            "Instalación de alumbrado industrial para bodega logística con áreas de operación y maniobra."
        ),
        "description": (
            "Proyecto de alumbrado industrial para mejorar visibilidad, seguridad operativa y mantenimiento "
            "en bodega logística."
        ),
        "client_name": "Centro logístico confidencial",
        "client_is_confidential": True,
        "sector": Sector.logistics,
        "service_type": ServiceType.industrial_lighting,
        "voltage_type": VoltageType.low_voltage,
        "location_city": "Chihuahua",
        "location_state": "Chihuahua",
        "status": ProjectStatus.completed,
        "is_featured": True,
        "is_published": True,
        "cover_image_url": "/uploads/demo/alumbrado-bodega.webp",
        "gallery_images": ["/uploads/demo/alumbrado-bodega-1.webp"],
        "technical_scope": (
            "Instalación de luminarias, canalización, circuitos de alumbrado, pruebas funcionales "
            "y documentación de avance."
        ),
        "deliverables": [
            "Planeación de rutas",
            "Instalación de luminarias",
            "Pruebas de encendido",
            "Memoria fotográfica",
        ],
        "challenges": "Alturas de trabajo y operación logística en paralelo.",
        "solution": "Se coordinó acceso por zonas y uso de equipo adecuado para instalación segura en altura.",
        "results": "Bodega con alumbrado funcional, ordenado y documentado para operación diaria.",
    },
]


def seed() -> None:
    db = SessionLocal()
    try:
        for item in PROJECTS:
            slug = slugify(f'{item["title"]} {item["location_city"]}')
            exists = db.scalar(select(Project.id).where(Project.slug == slug))
            if exists:
                continue

            project = Project(
                **item,
                slug=slug,
                seo_title=f'{item["title"]} | Norte Firme',
                seo_description=item["short_description"][:160],
                seo_keywords=[
                    item["title"],
                    item["sector"].value,
                    item["service_type"].value,
                    item["voltage_type"].value,
                ],
            )
            db.add(project)
        db.commit()
        print("Seed demo cargado correctamente.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
