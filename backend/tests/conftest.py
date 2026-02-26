import os

# Override env vars before any app modules are imported.
# The .env file sets a placeholder webhook secret which causes
# tests to fail on signature verification.
os.environ["CLERK_WEBHOOK_SECRET"] = ""
os.environ["CLERK_JWKS_URL"] = ""

import pytest  # noqa: E402
from sqlalchemy import text  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Import all models so they're registered with Base
import app.models  # noqa: F401, E402
from app.models.base import Base  # noqa: E402

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://beacon:beacon@localhost:5433/beacon_test",
)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db(test_engine) -> AsyncSession:
    """Provide a transactional database session that rolls back after each test."""
    session_factory = async_sessionmaker(test_engine, expire_on_commit=False)
    async with session_factory() as session, session.begin():
        yield session
        await session.rollback()
