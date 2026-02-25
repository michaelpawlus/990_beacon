"""Reusable test data factories."""
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Filing, FilingGrant, FilingPerson, Organization
from app.models.user import User


async def create_test_user(db: AsyncSession, **kwargs) -> User:
    defaults = {
        "clerk_id": f"clerk_{uuid.uuid4().hex[:8]}",
        "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
        "full_name": "Test User",
        "plan_tier": "free",
    }
    defaults.update(kwargs)
    user = User(**defaults)
    db.add(user)
    await db.flush()
    return user


async def create_test_org(db: AsyncSession, **kwargs) -> Organization:
    defaults = {
        "ein": f"{uuid.uuid4().int % 10**9:09d}",
        "name": "Test Organization",
        "city": "New York",
        "state": "NY",
        "ntee_code": "A01",
    }
    defaults.update(kwargs)
    org = Organization(**defaults)
    db.add(org)
    await db.flush()
    return org


async def create_test_filing(db: AsyncSession, org: Organization, **kwargs) -> Filing:
    defaults = {
        "organization_id": org.id,
        "object_id": f"obj_{uuid.uuid4().hex[:12]}",
        "tax_year": 2023,
        "filing_type": "990",
        "total_revenue": 1000000,
        "total_expenses": 900000,
        "net_assets": 500000,
        "contributions_and_grants": 800000,
        "program_service_revenue": 100000,
        "investment_income": 50000,
        "program_expenses": 700000,
        "management_expenses": 100000,
        "fundraising_expenses": 100000,
        "num_employees": 50,
        "num_volunteers": 100,
    }
    defaults.update(kwargs)
    filing = Filing(**defaults)
    db.add(filing)
    await db.flush()
    return filing


async def create_test_person(
    db: AsyncSession, filing: Filing, **kwargs
) -> FilingPerson:
    defaults = {
        "filing_id": filing.id,
        "name": "John Director",
        "title": "Board Member",
        "compensation": 0,
        "is_director": True,
        "is_officer": False,
        "is_key_employee": False,
        "is_highest_compensated": False,
    }
    defaults.update(kwargs)
    person = FilingPerson(**defaults)
    db.add(person)
    await db.flush()
    return person


async def create_test_grant(
    db: AsyncSession, filing: Filing, **kwargs
) -> FilingGrant:
    defaults = {
        "filing_id": filing.id,
        "recipient_name": "Grant Recipient Org",
        "recipient_ein": "987654321",
        "recipient_city": "Chicago",
        "recipient_state": "IL",
        "amount": 50000,
        "purpose": "General support",
    }
    defaults.update(kwargs)
    grant = FilingGrant(**defaults)
    db.add(grant)
    await db.flush()
    return grant
