"""User endpoint tests."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.asyncio
async def test_me_without_auth_returns_403():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/me")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_me_with_invalid_token_returns_403():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            "/api/v1/me",
            headers={"Authorization": "Bearer not-a-valid-jwt"},
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_me_with_unknown_clerk_id_returns_401(db, test_engine):
    """Token passes auth guard but clerk_id not in DB."""
    from fastapi_clerk_auth import HTTPAuthorizationCredentials

    from app.core.database import get_db
    from app.core.deps import clerk_auth_guard

    async def override_guard():
        return HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="fake-token",
            decoded={"sub": "user_nonexistent"},
        )

    async def override_get_db():
        yield db

    app.dependency_overrides[clerk_auth_guard] = override_guard
    app.dependency_overrides[get_db] = override_get_db

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get(
                "/api/v1/me",
                headers={"Authorization": "Bearer fake-token"},
            )

        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()
