import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_memory_endpoints():
    response = client.get("/api/memory")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_research_task():
    response = client.post(
        "/api/research",
        json={"user_query": "Compare self-attention vs recurrent models"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "created"
