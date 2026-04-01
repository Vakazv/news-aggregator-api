from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_get_news():
    response = client.get("/news/")
    assert response.status_code == 200


def test_create_news():
    payload = {
        "title": "Test title",
        "content": "Test content",
        "source": "Rambler",
        "tag": "media"
    }
    response = client.post("/news/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test title"