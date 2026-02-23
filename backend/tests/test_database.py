"""Database schema and migration tests.

These tests require a running PostgreSQL test instance (port 5433).
"""


import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Filing, Organization


def get_sync_test_url() -> str:
    """Convert async test URL to sync for tests."""
    return settings.TEST_DATABASE_URL.replace("+asyncpg", "+psycopg")


@pytest.fixture(scope="module")
def engine():
    url = get_sync_test_url()
    eng = create_engine(url)
    yield eng
    eng.dispose()


@pytest.fixture(scope="module")
def setup_schema(engine):
    """Run alembic upgrade head on the test database."""
    import os
    import subprocess

    env = os.environ.copy()
    env["DATABASE_URL_SYNC"] = get_sync_test_url()

    result = subprocess.run(
        ["uv", "run", "alembic", "upgrade", "head"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, f"Migration failed: {result.stderr}"
    yield
    # Downgrade after tests
    result = subprocess.run(
        ["uv", "run", "alembic", "downgrade", "base"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, f"Downgrade failed: {result.stderr}"


def test_migrations_upgrade_head(engine):
    """Test that alembic upgrade head succeeds."""
    import os
    import subprocess

    env = os.environ.copy()
    env["DATABASE_URL_SYNC"] = get_sync_test_url()

    result = subprocess.run(
        ["uv", "run", "alembic", "upgrade", "head"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, f"Migration failed: {result.stderr}"


def test_migrations_downgrade_base(engine):
    """Test that alembic downgrade base succeeds."""
    import os
    import subprocess

    env = os.environ.copy()
    env["DATABASE_URL_SYNC"] = get_sync_test_url()

    result = subprocess.run(
        ["uv", "run", "alembic", "downgrade", "base"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, f"Downgrade failed: {result.stderr}"


def test_migrations_round_trip(engine):
    """Test upgrade -> downgrade -> upgrade succeeds."""
    import os
    import subprocess

    env = os.environ.copy()
    env["DATABASE_URL_SYNC"] = get_sync_test_url()

    for cmd in ["upgrade head", "downgrade base", "upgrade head"]:
        result = subprocess.run(
            ["uv", "run", "alembic"] + cmd.split(),
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0, f"'{cmd}' failed: {result.stderr}"


def test_indexes_exist(engine):
    """Verify key indexes exist."""
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT indexname FROM pg_indexes "
                "WHERE tablename IN ('organizations', 'filings')"
            )
        )
        index_names = {row[0] for row in result}

    expected = {"idx_org_ein", "idx_org_name_trgm", "idx_filing_org", "idx_filing_year"}
    for idx in expected:
        assert idx in index_names, f"Missing index: {idx}"


def test_trigram_extension(engine):
    """Verify pg_trgm extension is installed."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT extname FROM pg_extension WHERE extname = 'pg_trgm'")
        )
        extensions = [row[0] for row in result]
    assert "pg_trgm" in extensions


def test_insert_and_query_organization(engine):
    """Test inserting and querying an organization."""
    with Session(engine) as session:
        org = Organization(
            ein="123456789",
            name="Test Foundation",
            city="Test City",
            state="CA",
        )
        session.add(org)
        session.commit()

        queried = session.query(Organization).filter_by(ein="123456789").first()
        assert queried is not None
        assert queried.name == "Test Foundation"

        session.delete(queried)
        session.commit()


def test_insert_filing_with_fk(engine):
    """Test inserting a filing with foreign key to organization."""
    with Session(engine) as session:
        org = Organization(
            ein="987654321",
            name="Filing Test Org",
            state="NY",
        )
        session.add(org)
        session.flush()

        filing = Filing(
            organization_id=org.id,
            object_id="test-filing-001",
            tax_year=2023,
            filing_type="990",
            total_revenue=1000000,
        )
        session.add(filing)
        session.commit()

        queried_filing = (
            session.query(Filing)
            .filter_by(object_id="test-filing-001")
            .first()
        )
        assert queried_filing is not None
        assert queried_filing.organization_id == org.id
        assert queried_filing.total_revenue == 1000000

        session.delete(queried_filing)
        session.delete(org)
        session.commit()
