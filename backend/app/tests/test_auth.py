def test_login_returns_access_token(client, db_session):
    from app.auth.models import UserRole
    from app.auth.schemas import UserCreate
    from app.auth.service import create_user

    create_user(
        db_session,
        UserCreate(
            email="editor@example.com",
            full_name="Editor Norte Firme",
            password="Password123!",
            role=UserRole.editor,
        ),
    )

    response = client.post("/api/v1/auth/login", json={"email": "editor@example.com", "password": "Password123!"})

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]
