import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert "WasmBox" in response.json()["message"]


def test_auth_register():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code in [200, 400]


def test_plugins_create():
    response = client.post("/api/plugin", json={
        "name": "test_plugin",
        "source_code": "print('hello')",
        "owner": "test"
    })
    assert response.status_code == 201
