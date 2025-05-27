"""Tests for the health check endpoint."""

from fastapi.testclient import TestClient
from src.interfaces.http.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "flow-logic-service",
        "environment": "development"
    }