from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.auth.models import User
from app.common.exceptions import bad_request, not_found
from app.core.config import settings
from app.projects.models import AssetType, Project, ProjectAsset
from app.projects.schemas import ProjectAssetCreate
from app.projects.service import log_action

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "application/pdf": ".pdf",
}

IMAGE_ASSET_TYPES = {
    AssetType.cover_image,
    AssetType.gallery_image,
    AssetType.before_image,
    AssetType.after_image,
    AssetType.delivery_evidence,
}
DOCUMENT_ASSET_TYPES = {AssetType.technical_document}


def validate_filename(filename: str) -> str:
    safe_name = Path(filename).name
    if safe_name != filename or not safe_name:
        raise bad_request("Nombre de archivo inválido.")
    return safe_name


def storage_root() -> Path:
    root = Path(settings.upload_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


async def save_upload(file: UploadFile, project_id: int) -> tuple[str, str]:
    original_name = validate_filename(file.filename or "archivo")
    extension = ALLOWED_CONTENT_TYPES.get(file.content_type or "")
    if not extension:
        raise bad_request("Tipo de archivo no permitido. Usa JPG, PNG, WEBP o PDF.")

    max_size = settings.max_upload_size_mb * 1024 * 1024
    content = await file.read()
    if len(content) > max_size:
        raise bad_request(f"El archivo supera el límite de {settings.max_upload_size_mb} MB.")

    detected_extension = detect_file_extension(content)
    if detected_extension != extension:
        raise bad_request("El contenido del archivo no coincide con su tipo declarado.")

    project_dir = storage_root() / str(project_id)
    project_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid4().hex}{extension}"
    destination = (project_dir / stored_name).resolve()

    if storage_root() not in destination.parents:
        raise bad_request("Ruta de archivo inválida.")

    destination.write_bytes(content)
    return f"/uploads/{project_id}/{stored_name}", original_name


def detect_file_extension(content: bytes) -> str | None:
    if content.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if content.startswith(b"RIFF") and content[8:12] == b"WEBP":
        return ".webp"
    if content.startswith(b"%PDF"):
        return ".pdf"
    return None


def validate_asset_file_type(asset_type: AssetType, content_type: str | None) -> None:
    extension = ALLOWED_CONTENT_TYPES.get(content_type or "")
    if asset_type in IMAGE_ASSET_TYPES and extension not in {".jpg", ".png", ".webp"}:
        raise bad_request("Este tipo de evidencia requiere una imagen JPG, PNG o WEBP.")
    if asset_type in DOCUMENT_ASSET_TYPES and extension != ".pdf":
        raise bad_request("Los documentos técnicos deben subirse en PDF.")


def list_assets(db: Session, project_id: int) -> list[ProjectAsset]:
    if not db.get(Project, project_id):
        raise not_found("Proyecto no encontrado.")
    return (
        db.query(ProjectAsset)
        .filter(ProjectAsset.project_id == project_id)
        .order_by(ProjectAsset.sort_order.asc(), ProjectAsset.created_at.desc())
        .all()
    )


async def create_asset(
    db: Session, project_id: int, payload: ProjectAssetCreate, file: UploadFile, user: User
) -> ProjectAsset:
    project = db.get(Project, project_id)
    if not project:
        raise not_found("Proyecto no encontrado.")

    validate_asset_file_type(payload.asset_type, file.content_type)
    url, original_name = await save_upload(file, project_id)
    asset = ProjectAsset(
        project_id=project_id,
        asset_type=payload.asset_type,
        url=url,
        filename=original_name,
        description=payload.description,
        sort_order=payload.sort_order,
    )
    db.add(asset)

    if payload.asset_type == AssetType.cover_image:
        project.cover_image_url = url
    elif payload.asset_type == AssetType.gallery_image:
        project.gallery_images = [*project.gallery_images, url]

    db.flush()
    log_action(
        db, user, "asset_uploaded", "project_asset", asset.id, {"project_id": project_id, "filename": original_name}
    )
    db.commit()
    db.refresh(asset)
    return asset


def delete_asset(db: Session, project_id: int, asset_id: int, user: User) -> None:
    asset = db.get(ProjectAsset, asset_id)
    if not asset or asset.project_id != project_id:
        raise not_found("Asset no encontrado.")

    project = db.get(Project, project_id)
    if project and asset.asset_type == AssetType.cover_image and project.cover_image_url == asset.url:
        project.cover_image_url = None
    if project and asset.asset_type == AssetType.gallery_image:
        project.gallery_images = [url for url in project.gallery_images if url != asset.url]

    relative = asset.url.removeprefix("/uploads/")
    file_path = (storage_root() / relative).resolve()
    if storage_root() in file_path.parents and file_path.exists():
        file_path.unlink()

    log_action(db, user, "asset_deleted", "project_asset", asset.id, {"project_id": project_id})
    db.delete(asset)
    db.commit()
