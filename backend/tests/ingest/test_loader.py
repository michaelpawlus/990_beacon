"""Tests for the database loader."""

import os

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# Import all models so SQLAlchemy knows about them
import app.models  # noqa: F401
from app.models.base import Base
from app.models.organization import Filing, FilingGrant, FilingPerson, Organization
from scripts.ingest.loader import load_filing
from scripts.ingest.xml_parser import ParsedFiling, ParsedGrant, ParsedPerson

TEST_DB_URL = os.environ.get(
    "DATABASE_URL_SYNC",
    "postgresql+psycopg://beacon:beacon@localhost:5433/beacon_test",
)


@pytest.fixture(scope="module")
def engine():
    from sqlalchemy import text

    eng = create_engine(TEST_DB_URL)
    with eng.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
    Base.metadata.create_all(eng)
    yield eng
    # Don't drop tables here — session-scoped conftest fixture handles cleanup
    eng.dispose()


@pytest.fixture
def session(engine):
    with Session(engine) as sess:
        # Use a savepoint so we can roll back each test
        sess.begin_nested()
        yield sess
        sess.rollback()


def _make_parsed_filing(**overrides) -> ParsedFiling:
    defaults = dict(
        ein="123456789",
        name="Test Organization",
        city="New York",
        state="NY",
        tax_year=2022,
        form_type="990",
        total_revenue=5_000_000,
        total_expenses=4_500_000,
        net_assets=2_000_000,
    )
    defaults.update(overrides)
    return ParsedFiling(**defaults)


class TestLoadFiling:
    def test_creates_org_and_filing(self, session):
        parsed = _make_parsed_filing()
        result = load_filing(session, parsed, "obj-001")

        assert result is True

        org = session.execute(
            select(Organization).where(Organization.ein == "123456789")
        ).scalar_one()
        assert org.name == "Test Organization"
        assert org.city == "New York"
        assert org.state == "NY"

        filing = session.execute(
            select(Filing).where(Filing.object_id == "obj-001")
        ).scalar_one()
        assert filing.organization_id == org.id
        assert filing.tax_year == 2022
        assert filing.total_revenue == 5_000_000

    def test_upserts_org_on_same_ein(self, session):
        parsed1 = _make_parsed_filing(name="First Name")
        load_filing(session, parsed1, "obj-002")

        parsed2 = _make_parsed_filing(name="Updated Name")
        load_filing(session, parsed2, "obj-003")

        orgs = session.execute(
            select(Organization).where(Organization.ein == "123456789")
        ).scalars().all()
        assert len(orgs) == 1
        assert orgs[0].name == "Updated Name"

        filings = session.execute(
            select(Filing).where(Filing.organization_id == orgs[0].id)
        ).scalars().all()
        assert len(filings) == 2

    def test_skips_duplicate_object_id(self, session):
        parsed = _make_parsed_filing()
        result1 = load_filing(session, parsed, "obj-004")
        result2 = load_filing(session, parsed, "obj-004")

        assert result1 is True
        assert result2 is False

        filings = session.execute(
            select(Filing).where(Filing.object_id == "obj-004")
        ).scalars().all()
        assert len(filings) == 1

    def test_creates_people(self, session):
        parsed = _make_parsed_filing(
            people=[
                ParsedPerson(
                    name="Jane Smith",
                    title="CEO",
                    compensation=250_000,
                    is_officer=True,
                ),
                ParsedPerson(
                    name="John Doe",
                    title="Board Chair",
                    is_director=True,
                ),
            ]
        )
        load_filing(session, parsed, "obj-005")

        filing = session.execute(
            select(Filing).where(Filing.object_id == "obj-005")
        ).scalar_one()

        people = session.execute(
            select(FilingPerson).where(FilingPerson.filing_id == filing.id)
        ).scalars().all()
        assert len(people) == 2
        names = {p.name for p in people}
        assert names == {"Jane Smith", "John Doe"}

    def test_creates_grants(self, session):
        parsed = _make_parsed_filing(
            form_type="990PF",
            grants=[
                ParsedGrant(
                    recipient_name="Local School",
                    recipient_city="New York",
                    recipient_state="NY",
                    amount=100_000,
                    purpose="Education",
                ),
            ],
        )
        load_filing(session, parsed, "obj-006")

        filing = session.execute(
            select(Filing).where(Filing.object_id == "obj-006")
        ).scalar_one()

        grants = session.execute(
            select(FilingGrant).where(FilingGrant.filing_id == filing.id)
        ).scalars().all()
        assert len(grants) == 1
        assert grants[0].recipient_name == "Local School"
        assert grants[0].amount == 100_000
        assert grants[0].purpose == "Education"

    def test_raw_xml_url_is_none(self, session):
        parsed = _make_parsed_filing()
        load_filing(session, parsed, "obj-007")

        filing = session.execute(
            select(Filing).where(Filing.object_id == "obj-007")
        ).scalar_one()
        assert filing.raw_xml_url is None
