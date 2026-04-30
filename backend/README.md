# Norte Firme API

Backend profesional para administrar proyectos y evidencia técnica de **Norte Firme Infraestructura y Construcción**. La API alimenta la sección de proyectos de `nortefirme.com.mx` y permite operar un portafolio privado con autenticación JWT.

## Stack

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Pydantic v2
- JWT con `python-jose`
- Passlib/bcrypt
- Docker y Docker Compose
- Pytest
- Ruff

## Arquitectura

```text
backend/
  app/
    core/        configuración, seguridad y base de datos
    auth/        usuarios, login, JWT y roles
    projects/    CRUD, filtros, SEO y auditoría
    uploads/     assets locales con abstracción migrable a S3/R2/MinIO
    common/      paginación y excepciones
    tests/       pruebas
  alembic/       migraciones
```

## Variables de entorno

Copia el ejemplo:

```bash
cp .env.example .env
```

En producción cambia `JWT_SECRET_KEY`, restringe `ALLOW_ADMIN_REGISTRATION=false` después de crear el administrador inicial y ajusta `CORS_ORIGINS`.

## Levantar con Docker

```bash
docker compose up --build
```

API:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

## Levantar sin Docker

Para desarrollo local sin PostgreSQL ni Docker, cambia temporalmente `DATABASE_URL` en `.env`:

```bash
DATABASE_URL=sqlite+pysqlite:///./nortefirme_dev.db
```

Luego:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

## Migraciones

Docker ejecuta `alembic upgrade head` al iniciar. Manualmente:

```bash
alembic upgrade head
```

## Crear administrador

Con `ALLOW_ADMIN_REGISTRATION=true`:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@nortefirme.com.mx",
    "full_name": "Administrador Norte Firme",
    "password": "CambiaEstaClave123",
    "role": "admin"
  }'
```

Después cambia `ALLOW_ADMIN_REGISTRATION=false`.

## Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@nortefirme.com.mx","password":"CambiaEstaClave123"}'
```

Usa el token:

```bash
Authorization: Bearer <token>
```

## Seed demo

```bash
python -m app.seed
```

Incluye cinco proyectos adaptados a infraestructura eléctrica:

- Instalación eléctrica en nave industrial
- Adecuación de tableros eléctricos comerciales
- Mantenimiento preventivo de subestación
- Sistema de puesta a tierra para edificio corporativo
- Alumbrado industrial en bodega logística

## Endpoints principales

Públicos:

```text
GET /api/v1/public/projects
GET /api/v1/public/projects/featured
GET /api/v1/public/projects/{slug}
```

Administración:

```text
GET    /api/v1/admin/projects
POST   /api/v1/admin/projects
GET    /api/v1/admin/projects/{id}
PUT    /api/v1/admin/projects/{id}
PATCH  /api/v1/admin/projects/{id}/publish
PATCH  /api/v1/admin/projects/{id}/unpublish
PATCH  /api/v1/admin/projects/{id}/feature
PATCH  /api/v1/admin/projects/{id}/unfeature
DELETE /api/v1/admin/projects/{id}
```

Assets:

```text
POST   /api/v1/admin/projects/{project_id}/assets
GET    /api/v1/admin/projects/{project_id}/assets
DELETE /api/v1/admin/projects/{project_id}/assets/{asset_id}
```

## Subir imágenes al portafolio

Los assets requieren JWT y validan el contenido real del archivo, no solo la extensión. Formatos permitidos:

- Imágenes: JPG, PNG, WEBP
- Documentos técnicos: PDF

Tipos de asset:

```text
cover_image
gallery_image
before_image
after_image
technical_document
delivery_evidence
```

Subir portada de proyecto:

```bash
curl -X POST http://localhost:8000/api/v1/admin/projects/1/assets \
  -H "Authorization: Bearer <token>" \
  -F "asset_type=cover_image" \
  -F "description=Portada para portafolio" \
  -F "sort_order=0" \
  -F "file=@/ruta/a/portada.webp;type=image/webp"
```

Subir imagen de galería:

```bash
curl -X POST http://localhost:8000/api/v1/admin/projects/1/assets \
  -H "Authorization: Bearer <token>" \
  -F "asset_type=gallery_image" \
  -F "description=Tableros instalados y canalización terminada" \
  -F "sort_order=1" \
  -F "file=@/ruta/a/evidencia.jpg;type=image/jpeg"
```

Subir evidencia de entrega:

```bash
curl -X POST http://localhost:8000/api/v1/admin/projects/1/assets \
  -H "Authorization: Bearer <token>" \
  -F "asset_type=delivery_evidence" \
  -F "description=Memoria fotográfica de entrega" \
  -F "sort_order=2" \
  -F "file=@/ruta/a/entrega.png;type=image/png"
```

Subir documento técnico PDF:

```bash
curl -X POST http://localhost:8000/api/v1/admin/projects/1/assets \
  -H "Authorization: Bearer <token>" \
  -F "asset_type=technical_document" \
  -F "description=Documento técnico de entrega" \
  -F "file=@/ruta/a/entrega-tecnica.pdf;type=application/pdf"
```

Al subir `cover_image`, el backend actualiza `cover_image_url` del proyecto. Al subir `gallery_image`, agrega la URL a `gallery_images`. Las respuestas públicas también incluyen `assets` para que el frontend pueda mostrar portada, galería, antes/después y evidencias.

## Filtros

```text
GET /api/v1/public/projects?page=1&limit=12
GET /api/v1/public/projects?sector=industrial
GET /api/v1/public/projects?service_type=substation
GET /api/v1/public/projects?voltage_type=medium_voltage
GET /api/v1/admin/projects?status=completed
GET /api/v1/admin/projects?is_featured=true
GET /api/v1/admin/projects?search=tableros
```

Formato de listas:

```json
{
  "items": [],
  "page": 1,
  "limit": 12,
  "total": 45,
  "pages": 4
}
```

## Crear proyecto

```bash
curl -X POST http://localhost:8000/api/v1/admin/projects \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Instalación eléctrica en nave industrial",
    "short_description": "Infraestructura eléctrica de baja tensión para nave industrial.",
    "description": "Ejecución de canalizaciones, alimentadores, tableros y pruebas de continuidad.",
    "client_name": "Cliente industrial confidencial",
    "client_is_confidential": true,
    "sector": "industrial",
    "service_type": "low_voltage_installation",
    "voltage_type": "low_voltage",
    "location_city": "Chihuahua",
    "location_state": "Chihuahua",
    "status": "completed",
    "is_featured": true,
    "is_published": false,
    "cover_image_url": "/uploads/demo/nave.webp",
    "deliverables": ["Levantamiento técnico", "Memoria fotográfica", "Entrega técnica"]
  }'
```

## Roadmap

- Panel administrativo web.
- Almacenamiento S3, Cloudflare R2 o MinIO.
- Versionado de documentos de entrega.
- Webhooks para reconstruir frontend estático.
- Métricas de visualización de proyectos.
