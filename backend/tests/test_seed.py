"""Seed script tests. Require running test database with migrations applied."""

import os
import subprocess

import pytest


def get_test_env():
    """Get environment with test database URL."""
    env = os.environ.copy()
    env["DATABASE_URL"] = env.get(
        "TEST_DATABASE_URL",
        "postgresql+asyncpg://beacon:beacon@localhost:5433/beacon_test",
    )
    env["DATABASE_URL_SYNC"] = env["DATABASE_URL"].replace("+asyncpg", "+psycopg")
    return env


@pytest.mark.skipif(
    not os.environ.get("RUN_DB_TESTS"),
    reason="Set RUN_DB_TESTS=1 to run DB-dependent tests",
)
def test_seed_runs_without_error():
    env = get_test_env()
    result = subprocess.run(
        ["uv", "run", "python", "scripts/seed.py"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, f"Seed failed: {result.stderr}"
    assert "Seed complete!" in result.stdout


@pytest.mark.skipif(
    not os.environ.get("RUN_DB_TESTS"),
    reason="Set RUN_DB_TESTS=1 to run DB-dependent tests",
)
def test_seed_is_idempotent():
    env = get_test_env()
    # Run twice
    for _ in range(2):
        result = subprocess.run(
            ["uv", "run", "python", "scripts/seed.py"],
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0, f"Seed failed: {result.stderr}"
