import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from tests.factories import create_test_filing, create_test_org, create_test_user


@pytest.fixture
async def auth_client(db, test_engine):
    """Create an authenticated test client."""
    from app.core.database import get_db
    from app.core.deps import get_current_user

    user = await create_test_user(db, clerk_id="test_search_user")

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
        yield client

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


class TestSearchEndpoint:
    @pytest.mark.asyncio
    async def test_search_requires_auth(self, unauth_client):
        response = await unauth_client.get("/api/v1/search")
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_search_by_name(self, auth_client, db):
        org = await create_test_org(db, name="American Red Cross", ein="530196605")
        await create_test_filing(db, org, tax_year=2023)
        await db.flush()

        response = await auth_client.get(
            "/api/v1/search", params={"q": "Red Cross"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert any(
            item["name"] == "American Red Cross" for item in data["items"]
        )

    @pytest.mark.asyncio
    async def test_search_fuzzy_match(self, auth_client, db):
        org = await create_test_org(
            db, name="American Red Cross", ein="530196606"
        )
        await create_test_filing(db, org, tax_year=2023)
        await db.flush()

        # Use a query close enough for pg_trgm default threshold (0.3)
        response = await auth_client.get(
            "/api/v1/search", params={"q": "American Rd Cross"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    @pytest.mark.asyncio
    async def test_search_filter_by_state(self, auth_client, db):
        org_ny = await create_test_org(
            db, name="NY Org Search", state="NY", ein="111111111"
        )
        org_ca = await create_test_org(
            db, name="CA Org Search", state="CA", ein="222222222"
        )
        await create_test_filing(db, org_ny)
        await create_test_filing(db, org_ca)
        await db.flush()

        response = await auth_client.get(
            "/api/v1/search", params={"q": "Org Search", "state": "NY"}
        )
        assert response.status_code == 200
        data = response.json()
        names = [item["name"] for item in data["items"]]
        assert "NY Org Search" in names
        assert "CA Org Search" not in names

    @pytest.mark.asyncio
    async def test_search_filter_by_ntee(self, auth_client, db):
        org = await create_test_org(
            db, name="NTEE Test Org", ntee_code="B20", ein="333333333"
        )
        await create_test_filing(db, org)
        await db.flush()

        response = await auth_client.get(
            "/api/v1/search", params={"q": "NTEE Test", "ntee_code": "B20"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    @pytest.mark.asyncio
    async def test_search_pagination(self, auth_client, db):
        for i in range(5):
            org = await create_test_org(
                db, name=f"Pagination Org {i}", ein=f"44444444{i}"
            )
            await create_test_filing(db, org)
        await db.flush()

        response = await auth_client.get(
            "/api/v1/search",
            params={"q": "Pagination Org", "page_size": 2, "page": 1},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] >= 5
        assert data["page"] == 1

    @pytest.mark.asyncio
    async def test_search_empty_query(self, auth_client, db):
        response = await auth_client.get("/api/v1/search")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data

    @pytest.mark.asyncio
    async def test_search_no_results(self, auth_client, db):
        response = await auth_client.get(
            "/api/v1/search", params={"q": "xyznonexistent12345"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []


class TestTypeaheadEndpoint:
    @pytest.mark.asyncio
    async def test_typeahead_requires_auth(self, unauth_client):
        response = await unauth_client.get(
            "/api/v1/search/typeahead", params={"q": "test"}
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_typeahead_returns_matches(self, auth_client, db):
        await create_test_org(
            db, name="Typeahead Test Org", ein="555555555"
        )
        await db.flush()

        response = await auth_client.get(
            "/api/v1/search/typeahead", params={"q": "Typeahead"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["name"] == "Typeahead Test Org"

    @pytest.mark.asyncio
    async def test_typeahead_min_query_length(self, auth_client):
        response = await auth_client.get(
            "/api/v1/search/typeahead", params={"q": "a"}
        )
        assert response.status_code == 422  # FastAPI validation error

    @pytest.mark.asyncio
    async def test_typeahead_limit(self, auth_client, db):
        for i in range(15):
            await create_test_org(
                db, name=f"Limit Test Org {i}", ein=f"66666{i:04d}"
            )
        await db.flush()

        response = await auth_client.get(
            "/api/v1/search/typeahead", params={"q": "Limit Test"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 10
