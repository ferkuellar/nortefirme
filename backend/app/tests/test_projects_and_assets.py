PROJECT_PAYLOAD = {
    "title": "Instalación eléctrica en nave industrial",
    "short_description": "Infraestructura eléctrica en baja tensión para nave industrial en Chihuahua.",
    "description": "Suministro e instalación de alimentadores, tableros derivados y canalización EMT.",
    "client_name": "Cliente industrial confidencial",
    "client_is_confidential": True,
    "voltage_type": "low_voltage",
    "location_city": "Chihuahua",
    "location_state": "Chihuahua",
    "status": "completed",
    "technical_scope": "Canalizaciones, alimentadores principales, tableros y pruebas de continuidad.",
    "deliverables": "Levantamiento técnico, memoria fotográfica, entrega técnica",
    "results": "Instalación entregada con orden técnico y evidencia de avance.",
}


def create_project(client, headers, payload=None):
    response = client.post("/api/v1/admin/projects", json=payload or PROJECT_PAYLOAD, headers=headers)
    assert response.status_code == 200
    return response.json()


def upload_png(client, headers, project_id, asset_type="cover_image"):
    content = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32
    response = client.post(
        f"/api/v1/admin/projects/{project_id}/assets",
        headers=headers,
        data={"asset_type": asset_type, "description": "Evidencia fotografica"},
        files={"file": ("tablero.png", content, "image/png")},
    )
    assert response.status_code == 200
    return response.json()


def test_create_publish_and_query_public_project(client, admin_headers):
    project = create_project(client, admin_headers)
    upload_png(client, admin_headers, project["id"])

    publish = client.patch(f"/api/v1/admin/projects/{project['id']}/publish", headers=admin_headers)
    assert publish.status_code == 200

    feature = client.patch(f"/api/v1/admin/projects/{project['id']}/feature", headers=admin_headers)
    assert feature.status_code == 200

    public_list = client.get("/api/v1/public/projects")
    assert public_list.status_code == 200
    assert public_list.json()["total"] == 1

    featured = client.get("/api/v1/public/projects/featured")
    assert featured.status_code == 200
    assert featured.json()["total"] == 1

    detail = client.get(f"/api/v1/public/projects/{project['slug']}")
    assert detail.status_code == 200
    assert detail.json()["assets"][0]["asset_type"] == "cover_image"


def test_unpublished_project_is_not_public(client, admin_headers):
    create_project(client, admin_headers)

    public_list = client.get("/api/v1/public/projects")

    assert public_list.status_code == 200
    assert public_list.json()["total"] == 0


def test_project_must_be_completed_to_be_public(client, admin_headers):
    payload = PROJECT_PAYLOAD | {"status": "in_progress"}
    project = create_project(client, admin_headers, payload)
    upload_png(client, admin_headers, project["id"])

    publish = client.patch(f"/api/v1/admin/projects/{project['id']}/publish", headers=admin_headers)
    assert publish.status_code == 200

    public_list = client.get("/api/v1/public/projects")
    assert public_list.json()["total"] == 0


def test_upload_valid_asset_updates_cover_image(client, admin_headers):
    project = create_project(client, admin_headers)

    asset = upload_png(client, admin_headers, project["id"])
    detail = client.get(f"/api/v1/admin/projects/{project['id']}", headers=admin_headers)

    assert asset["url"].endswith(".png")
    assert detail.json()["cover_image_url"] == asset["url"]


def test_reject_invalid_asset_content(client, admin_headers):
    project = create_project(client, admin_headers)

    response = client.post(
        f"/api/v1/admin/projects/{project['id']}/assets",
        headers=admin_headers,
        data={"asset_type": "cover_image"},
        files={"file": ("tablero.png", b"not a real png", "image/png")},
    )

    assert response.status_code == 400


def test_reject_pdf_as_cover_image(client, admin_headers):
    project = create_project(client, admin_headers)

    response = client.post(
        f"/api/v1/admin/projects/{project['id']}/assets",
        headers=admin_headers,
        data={"asset_type": "cover_image"},
        files={"file": ("memoria.pdf", b"%PDF-1.4\n", "application/pdf")},
    )

    assert response.status_code == 400
