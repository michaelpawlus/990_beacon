import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from tests.factories import (
    create_test_filing,
    create_test_grant,
    create_test_org,
    create_test_person,
    create_test_user,
)


@pytest.fixture
async def auth_client(db, test_engine):
    from app.core.database import get_db
    from app.core.deps import get_current_user

    user = await create_test_user(db, clerk_id="test_org_user")

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


class TestOrganizationProfile:
    @pytest.mark.asyncio
    async def test_get_organization(self, auth_client, db):
        org = await create_test_org(
            db, name="Profile Test Org", ein="777777777"
        )
        await create_test_filing(
            db, org, tax_year=2021, object_id="obj_2021"
        )
        await create_test_filing(
            db, org, tax_year=2022, object_id="obj_2022"
        )
        f3 = await create_test_filing(
            db, org, tax_year=2023, object_id="obj_2023"
        )
        await create_test_person(
            db, f3, name="CEO Person", title="CEO", compensation=200000
        )
        await db.flush()

        response = await auth_client.get(f"/api/v1/organizations/{org.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Profile Test Org"
        assert data["ein"] == "777777777"
        assert len(data["filings"]) == 3
        # Filings should be ordered by year desc
        assert data["filings"][0]["tax_year"] == 2023
        assert data["filings"][1]["tax_year"] == 2022
        assert data["filings"][2]["tax_year"] == 2021
        # Check people
        assert len(data["filings"][0]["people"]) == 1
        assert data["filings"][0]["people"][0]["name"] == "CEO Person"

    @pytest.mark.asyncio
    async def test_get_organization_with_grants(self, auth_client, db):
        org = await create_test_org(
            db, name="Foundation Test", ein="888888888"
        )
        filing = await create_test_filing(db, org, filing_type="990PF")
        await create_test_grant(
            db, filing, recipient_name="Grant Recipient", amount=100000
        )
        await db.flush()

        response = await auth_client.get(f"/api/v1/organizations/{org.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["filings"][0]["grants"]) == 1
        assert (
            data["filings"][0]["grants"][0]["recipient_name"]
            == "Grant Recipient"
        )
        assert data["filings"][0]["grants"][0]["amount"] == 100000

    @pytest.mark.asyncio
    async def test_get_organization_not_found(self, auth_client):
        fake_id = uuid.uuid4()
        response = await auth_client.get(f"/api/v1/organizations/{fake_id}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_organization_by_ein(self, auth_client, db):
        org = await create_test_org(
            db, name="EIN Lookup Org", ein="999999999"
        )
        await create_test_filing(db, org)
        await db.flush()

        response = await auth_client.get(
            "/api/v1/organizations/by-ein/999999999"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "EIN Lookup Org"

    @pytest.mark.asyncio
    async def test_get_organization_by_ein_not_found(self, auth_client):
        response = await auth_client.get(
            "/api/v1/organizations/by-ein/000000000"
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_organization_requires_auth(self, unauth_client, db):
        org = await create_test_org(db, ein="111222333")
        await db.flush()
        response = await unauth_client.get(f"/api/v1/organizations/{org.id}")
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_organization_metrics(self, auth_client, db):
        org = await create_test_org(
            db, name="Metrics Org", ein="444555666"
        )
        await create_test_filing(
            db,
            org,
            tax_year=2022,
            total_revenue=800000,
            total_expenses=750000,
            program_expenses=600000,
            fundraising_expenses=50000,
            object_id="met_2022",
        )
        await create_test_filing(
            db,
            org,
            tax_year=2023,
            total_revenue=1000000,
            total_expenses=900000,
            program_expenses=700000,
            fundraising_expenses=100000,
            object_id="met_2023",
        )
        await db.flush()

        response = await auth_client.get(f"/api/v1/organizations/{org.id}")
        assert response.status_code == 200
        data = response.json()
        metrics = data["metrics"]
        # program_expense_ratio = 700000 / 900000 ~ 0.778
        assert metrics["program_expense_ratio"] is not None
        assert abs(metrics["program_expense_ratio"] - 700000 / 900000) < 0.01
        # fundraising_efficiency = 100000 / 900000 ~ 0.111
        assert metrics["fundraising_efficiency"] is not None
        # revenue_growth_rate = (1000000 - 800000) / 800000 = 0.25
        assert metrics["revenue_growth_rate"] is not None
        assert abs(metrics["revenue_growth_rate"] - 0.25) < 0.01
