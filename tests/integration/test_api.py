from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    assert response.headers.get("X-Request-ID")


def test_current_user():
    response = client.get("/api/v1/users/me")
    assert response.status_code == 200
    assert response.json()["first_name"] == "Hazem"


def test_mock_chat():
    response = client.post("/api/v1/chat", json={"message": "Hello"})
    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "mock"
    assert body["conversation_id"]
    assert body["answer"]
