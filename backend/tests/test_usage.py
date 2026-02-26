"""Tests for usage tracking."""

import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from tests.factories import create_test_filing, create_test_org, create_test_user


@pytest.fixture
async def auth_client_with_user(db, test_engine):
    """Create an authenticated test client with unique user per test."""
    from app.core.database import get_db
    from app.core.deps import get_current_user

    unique_id = uuid.uuid4().hex[:8]
    user = await create_test_user(db, clerk_id=f"usage_{unique_id}")

    async def override_get_db():
        yield db

    async def override_auth():
        return user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_auth

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client, user

    app.dependency_overrides.clear()


@pytest.fixture
async def unauth_client(db, test_engine):
    """Create an unauthenticated test client."""
    from app.core.database import get_db

    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


class TestUsageTracking:
    async def test_search_creates_usage_event(self, auth_client_with_user, db):
        """Searching creates a usage event."""
        client, user = auth_client_with_user
        ein = f"9{uuid.uuid4().int % 10**8:08d}"
        org = await create_test_org(
            db, name="Usage Track Org", ein=ein
        )
        await create_test_filing(db, org)
        await db.flush()

        response = await client.get("/api/v1/search", params={"q": "Usage Track"})
        assert response.status_code == 200

        summary_resp = await client.get("/api/v1/usage/summary")
        assert summary_resp.status_code == 200
        data = summary_resp.json()
        assert data["searches_today"] >= 1
        assert data["searches_this_month"] >= 1

    async def test_profile_view_creates_usage_event(self, auth_client_with_user, db):
        """Viewing an org profile creates a usage event."""
        client, user = auth_client_with_user
        ein = f"9{uuid.uuid4().int % 10**8:08d}"
        org = await create_test_org(
            db, name="Usage Profile Org", ein=ein
        )
        await create_test_filing(db, org)
        await db.flush()

        response = await client.get(f"/api/v1/organizations/{org.id}")
        assert response.status_code == 200

        summary_resp = await client.get("/api/v1/usage/summary")
        assert summary_resp.status_code == 200
        data = summary_resp.json()
        assert data["profile_views_today"] >= 1
        assert data["profile_views_this_month"] >= 1

    async def test_usage_summary_filters_by_user(self, db, test_engine):
        """Usage summary only shows current user's events."""
        from app.core.database import get_db
        from app.core.deps import get_current_user

        uid1 = uuid.uuid4().hex[:8]
        uid2 = uuid.uuid4().hex[:8]
        user1 = await create_test_user(db, clerk_id=f"filter_{uid1}")
        user2 = await create_test_user(db, clerk_id=f"filter_{uid2}")
        ein = f"9{uuid.uuid4().int % 10**8:08d}"
        org = await create_test_org(
            db, name="Filter Org", ein=ein
        )
        await create_test_filing(db, org)
        await db.flush()

        async def override_get_db():
            yield db

        # User 1 does a search
        async def override_auth_user1():
            return user1

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_auth_user1

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client1:
            await client1.get("/api/v1/search", params={"q": "Filter"})

        # User 2 checks their summary - should be 0
        async def override_auth_user2():
            return user2

        app.dependency_overrides[get_current_user] = override_auth_user2

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client2:
            summary_resp = await client2.get("/api/v1/usage/summary")
            assert summary_resp.status_code == 200
            data = summary_resp.json()
            assert data["searches_today"] == 0

        app.dependency_overrides.clear()

    async def test_usage_summary_requires_auth(self, unauth_client):
        """Usage summary endpoint requires authentication."""
        response = await unauth_client.get("/api/v1/usage/summary")
        assert response.status_code == 403
