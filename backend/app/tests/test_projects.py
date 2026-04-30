PROJECT_PAYLOAD = {
    "title": "Instalación eléctrica en nave industrial",
    "slug": "instalacion-electrica-nave-industrial-chihuahua",
    "short_description": "Infraestructura eléctrica de baja tensión para nave industrial.",
    "description": "Instalación de alimentadores, canalizaciones, tableros derivados y pruebas de continuidad.",
    "client_name": "Cliente industrial confidencial",
    "client_is_confidential": True,
    "sector": "industrial",
    "service_type": "low_voltage_installation",
    "voltage_type": "low_voltage",
    "location_city": "Chihuahua",
    "location_state": "Chihuahua",
    "status": "completed",
    "is_featured": True,
    "is_published": False,
    "cover_image_url": "/uploads/demo/nave.webp",
    "technical_scope": "Suministro e instalación de alimentadores principales, canalización EMT y tableros.",
    "deliverables": ["Levantamiento técnico", "Montaje de tableros", "Memoria fotográfica", "Entrega técnica"],
    "challenges": "Coordinación con obra civil en operación.",
    "solution": "Planeación por etapas y revisión de rutas eléctricas.",
    "results": "Instalación ordenada, segura y documentada.",
}


def create_project(client, headers):
    response = client.post("/api/v1/admin/projects", json=PROJECT_PAYLOAD, headers=headers)
    assert response.status_code == 201
    return response.json()


def test_create_and_publish_project(client, auth_headers):
    project = create_project(client, auth_headers)

    publish = client.patch(f'/api/v1/admin/projects/{project["id"]}/publish', headers=auth_headers)

    assert publish.status_code == 200
    assert publish.json()["is_published"] is True


def test_public_projects_hide_unpublished_projects(client, auth_headers):
    create_project(client, auth_headers)

    response = client.get("/api/v1/public/projects")

    assert response.status_code == 200
    assert response.json()["total"] == 0


def test_public_projects_show_published_completed_projects(client, auth_headers):
    project = create_project(client, auth_headers)
    client.patch(f'/api/v1/admin/projects/{project["id"]}/publish', headers=auth_headers)

    response = client.get("/api/v1/public/projects")

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["slug"] == PROJECT_PAYLOAD["slug"]


def test_upload_valid_asset(client, auth_headers):
    project = create_project(client, auth_headers)

    response = client.post(
        f'/api/v1/admin/projects/{project["id"]}/assets',
        headers=auth_headers,
        data={"asset_type": "gallery_image", "description": "Evidencia en campo", "sort_order": "1"},
        files={"file": ("evidencia.webp", b"RIFF\x10\x00\x00\x00WEBPVP8 ", "image/webp")},
    )

    assert response.status_code == 201
    assert response.json()["asset_type"] == "gallery_image"
    assert response.json()["filename"] == "evidencia.webp"


def test_public_project_detail_includes_uploaded_assets(client, auth_headers):
    project = create_project(client, auth_headers)
    client.post(
        f'/api/v1/admin/projects/{project["id"]}/assets',
        headers=auth_headers,
        data={"asset_type": "cover_image", "description": "Portada de proyecto"},
        files={"file": ("portada.png", b"\x89PNG\r\n\x1a\n\x00\x00", "image/png")},
    )
    client.patch(f'/api/v1/admin/projects/{project["id"]}/publish', headers=auth_headers)

    response = client.get(f'/api/v1/public/projects/{PROJECT_PAYLOAD["slug"]}')

    assert response.status_code == 200
    assert response.json()["assets"][0]["asset_type"] == "cover_image"
    assert response.json()["cover_image_url"].startswith("/uploads/")


def test_reject_invalid_asset_file(client, auth_headers):
    project = create_project(client, auth_headers)

    response = client.post(
        f'/api/v1/admin/projects/{project["id"]}/assets',
        headers=auth_headers,
        data={"asset_type": "technical_document"},
        files={"file": ("malware.exe", b"not-allowed", "application/octet-stream")},
    )

    assert response.status_code == 400
