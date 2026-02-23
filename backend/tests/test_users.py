"""User endpoint tests."""

import jwt
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


def make_token(clerk_id: str = "user_test123") -> str:
    """Create a test JWT token."""
    return jwt.encode({"sub": clerk_id}, "test-secret", algorithm="HS256")


@pytest.mark.asyncio
async def test_me_without_auth_returns_401():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_invalid_token_returns_401():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/v1/me",
            headers={"Authorization": "Bearer not-a-valid-jwt"},
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_unknown_clerk_id_returns_401():
    """Token is valid JWT but clerk_id not in DB."""
    token = make_token("user_nonexistent")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 401
