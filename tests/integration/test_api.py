from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    assert response.headers.get("X-Request-ID")


def test_login_success():
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "hazem.hossam", "password": "password123"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"
    assert body["expires_in"] > 0


def test_login_invalid_credentials():
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "hazem.hossam", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_current_user_unauthorized():
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_current_user_authenticated():
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "hazem.hossam@example.com", "password": "password123"},
    )
    token = login_resp.json()["access_token"]

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Hazem"
    assert response.json()["username"] == "hazem.hossam"


def test_mohamed_login_and_current_user():
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "mohamed.abdelmonem", "password": "password123"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    assert token

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["id"] == "USR-002"
    assert user_data["username"] == "mohamed.abdelmonem"
    assert user_data["first_name"] == "Mohamed"
    assert user_data["last_name"] == "Abdelmonem"
    assert user_data["display_name"] == "Mohamed Abdelmonem"
    assert user_data["email"] == "mohamed.abdelmonem@example.com"



def test_mock_chat_unauthorized():
    response = client.post("/api/v1/chat", json={"message": "Hello"})
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_mock_chat_authenticated():
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "hazem.hossam", "password": "password123"},
    )
    token = login_resp.json()["access_token"]

    response = client.post(
        "/api/v1/chat",
        json={"message": "Hello"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "mock"
    assert body["conversation_id"]
    assert "Hazem" in body["answer"]


