"""Tests for the HTTP client."""

import pytest
from unittest.mock import patch
from src.infrastructure.services.http_client import HttpClient

@pytest.mark.asyncio
async def test_http_client_get():
    """Test the GET method of the HTTP client."""
    client = HttpClient(base_url="http://test.com")

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"data": "test"}

        response = await client.get("/endpoint")
        assert response == {"data": "test"}

@pytest.mark.asyncio
async def test_http_client_post():
    """Test the POST method of the HTTP client."""
    client = HttpClient(base_url="http://test.com")

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value.status_code = 201
        mock_request.return_value.json.return_value = {"id": 1}

        response = await client.post("/endpoint", json={"key": "value"})
        assert response == {"id": 1}

# AsyncMock helper for async testing
class AsyncMock:
    """Helper class for creating async mocks."""

    def __init__(self, *args, **kwargs):
        """Initialize the mock."""
        pass

    def __call__(self, *args, **kwargs):
        """Call the mock."""
        return self

    async def __aenter__(self):
        """Enter the async context."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the async context."""
        pass