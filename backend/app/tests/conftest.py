import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-with-enough-length"
os.environ["ALLOW_ADMIN_REGISTRATION"] = "true"

from app.auth.models import UserRole
from app.auth.schemas import UserCreate
from app.auth.service import create_user
from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app
from app.projects import models as project_models

_ = project_models


@pytest.fixture()
def db_session(tmp_path) -> Generator[Session, None, None]:
    settings.upload_dir = str(tmp_path / "uploads")
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def admin_token(client: TestClient, db_session: Session) -> str:
    create_user(
        db_session,
        UserCreate(
            email="admin@example.com",
            full_name="Admin Norte Firme",
            password="Password123!",
            role=UserRole.admin,
        ),
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "Password123!"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture()
def auth_headers(admin_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {admin_token}"}
