import os
import uuid
from pathlib import Path

from fastapi import UploadFile
from slugify import slugify

from app.common.enums import AssetType
from app.common.exceptions import BadRequestException
from app.core.config import settings

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "application/pdf"}
IMAGE_ASSET_TYPES = {
    AssetType.COVER_IMAGE,
    AssetType.GALLERY_IMAGE,
    AssetType.BEFORE_IMAGE,
    AssetType.AFTER_IMAGE,
    AssetType.DELIVERY_EVIDENCE,
}
DOCUMENT_ASSET_TYPES = {AssetType.TECHNICAL_DOCUMENT}
MAX_SIZE = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


class UploadService:
    @staticmethod
    def _detect_extension(content: bytes) -> str | None:
        if content.startswith(b"\xff\xd8\xff"):
            return "jpg"
        if content.startswith(b"\x89PNG\r\n\x1a\n"):
            return "png"
        if content.startswith(b"RIFF") and content[8:12] == b"WEBP":
            return "webp"
        if content.startswith(b"%PDF"):
            return "pdf"
        return None

    @staticmethod
    async def validate_and_save(file: UploadFile, asset_type: AssetType) -> tuple[str, str, int, str]:
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise BadRequestException("Invalid file type")

        content = await file.read()
        size = len(content)

        if size > MAX_SIZE:
            raise BadRequestException(f"File too large. Max {settings.MAX_UPLOAD_SIZE_MB}MB")
        if not file.filename:
            raise BadRequestException("Filename is required")

        detected_ext = UploadService._detect_extension(content)
        if detected_ext is None:
            raise BadRequestException("Invalid file content")

        original_ext = file.filename.rsplit(".", 1)[-1].lower()
        if original_ext == "jpeg":
            original_ext = "jpg"
        if original_ext not in {"jpg", "png", "webp", "pdf"}:
            raise BadRequestException("Invalid file extension")
        if original_ext != detected_ext:
            raise BadRequestException("File extension does not match file content")
        if asset_type in IMAGE_ASSET_TYPES and detected_ext == "pdf":
            raise BadRequestException("This asset type requires an image file")
        if asset_type in DOCUMENT_ASSET_TYPES and detected_ext != "pdf":
            raise BadRequestException("This asset type requires a PDF file")

        safe_name = slugify(Path(file.filename).stem) or "evidencia"
        ext = detected_ext
        unique_filename = f"{uuid.uuid4().hex[:8]}-{safe_name}.{ext}"

        if settings.UPLOAD_BACKEND == "local":
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            upload_dir = Path(settings.UPLOAD_DIR).resolve()
            filepath = (upload_dir / unique_filename).resolve()
            if upload_dir not in filepath.parents:
                raise BadRequestException("Invalid upload path")
            with open(filepath, "wb") as buffer:
                buffer.write(content)
            url = f"{settings.PUBLIC_UPLOAD_BASE_URL.rstrip('/')}/{unique_filename}"
            return url, unique_filename, size, file.content_type or "application/octet-stream"

        # Future S3/R2 implementation
        raise NotImplementedError("Only local upload is currently supported")
