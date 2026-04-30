# Norte Firme Backend API

Este es el backend profesional y modular para la plataforma de Norte Firme Infraestructura y Construcción. Está construido con Python 3.12+, FastAPI, y PostgreSQL, estructurado para ser limpio, escalable y seguro.

## Stack Tecnológico

- **Framework**: FastAPI
- **Base de datos**: PostgreSQL
- **ORM**: SQLAlchemy 2.x
- **Migraciones**: Alembic
- **Validación**: Pydantic v2
- **Autenticación**: JWT + Passlib (bcrypt)
- **Despliegue**: Docker & Docker Compose
- **Testing**: Pytest

## Arquitectura

El proyecto utiliza una arquitectura de capas separadas por dominio (Domain-Driven Structure):
- `app/api/`: Rutas de la API (Endpoints expuestos).
- `app/services/`: Lógica de negocio (Autenticación, validación de archivos, etc.).
- `app/repositories/`: Capa de acceso a datos (Llamadas a base de datos aisladas).
- `app/models/`: Modelos de SQLAlchemy (Base de datos).
- `app/schemas/`: Esquemas de Pydantic (Validación de entrada y salida).

## Instalación y Ejecución Local (con Docker)

Asegúrate de tener Docker y Docker Compose instalados y corriendo en tu máquina.

1.  **Variables de entorno**
    Copia el archivo de ejemplo:
    ```bash
    cp .env.example .env
    ```

2.  **Levantar servicios**
    Esto levantará FastAPI, PostgreSQL y pgAdmin.
    ```bash
    docker compose up -d --build
    ```

3.  **Ejecutar migraciones (Alembic)**
    Genera y aplica el esquema inicial en PostgreSQL:
    ```bash
    docker compose exec api alembic revision --autogenerate -m "initial schema"
    docker compose exec api alembic upgrade head
    ```

4.  **Cargar datos semilla (Seed)**
    Crea el administrador, servicios, sectores y proyectos de prueba:
    ```bash
    docker compose exec api python -m app.seed.seed_data
    ```

## Acceso

- **API Base URL**: `http://localhost:8000/api/v1`
- **Swagger UI (Documentación)**: `http://localhost:8000/docs`
- **pgAdmin**: `http://localhost:5050` (admin@nortefirme.com.mx / admin)

## Permisos y Roles

- `viewer`: Solo lectura (para dashboards futuros).
- `editor`: Puede crear, editar, publicar y subir imágenes, pero no borrar usuarios.
- `admin`: Control total (crear/borrar usuarios, proyectos, servicios, etc.).

## Usuario Demo
- **Email**: `admin@nortefirme.com.mx`
- **Password**: `ChangeMe123!`
*(¡Cambiar en producción!)*

## Scripts Útiles
- **Generar nueva migración**: `docker compose exec api alembic revision --autogenerate -m "descripcion"`
- **Aplicar migraciones**: `docker compose exec api alembic upgrade head`
- **Correr tests**: `docker compose exec api pytest`
