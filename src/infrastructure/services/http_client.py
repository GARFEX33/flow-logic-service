"""HTTP client for external service integration."""

import httpx
from typing import Any, Dict, Optional
import asyncio

class HttpClient:
    """Asynchronous HTTP client for making requests to external services."""

    def __init__(self, base_url: str, timeout: int = 30):
        """Initialize the HTTP client with a base URL and timeout."""
        self.base_url = base_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the specified endpoint."""
        try:
            response = await self.client.request(
                method=method,
                url=endpoint,
                headers=headers,
                params=params,
                json=json,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            # Handle HTTP errors here
            print(f"HTTP error occurred: {exc}")
            raise
        except Exception as exc:
            # Handle other errors here
            print(f"An error occurred: {exc}")
            raise
        finally:
            await self.client.aclose()

    async def get(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        """Make a GET request."""
        return await self.request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        """Make a POST request."""
        return await self.request("POST", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        """Make a PUT request."""
        return await self.request("PUT", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        """Make a DELETE request."""
        return await self.request("DELETE", endpoint, **kwargs)