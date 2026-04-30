def test_register_and_login_returns_tokens(client):
    register = client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin@nortefirme.com.mx",
            "full_name": "Administrador Norte Firme",
            "password": "Password123!",
            "role": "admin",
        },
    )
    assert register.status_code == 200

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@nortefirme.com.mx", "password": "Password123!"},
    )

    assert login.status_code == 200
    assert login.json()["access_token"]
    assert login.json()["refresh_token"]


def test_register_allows_only_initial_admin(client):
    first = client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin@nortefirme.com.mx",
            "full_name": "Administrador Norte Firme",
            "password": "Password123!",
            "role": "admin",
        },
    )
    second = client.post(
        "/api/v1/auth/register",
        json={
            "email": "editor@nortefirme.com.mx",
            "full_name": "Editor Norte Firme",
            "password": "Password123!",
            "role": "editor",
        },
    )

    assert first.status_code == 200
    assert second.status_code == 400
