from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ui_pages_are_served() -> None:
    with TestClient(app) as client:
        responses = [
            client.get("/"),
            client.get("/cases/new"),
            client.get("/cases/EXP-2026-001"),
        ]
    assert all(response.status_code == 200 for response in responses)
