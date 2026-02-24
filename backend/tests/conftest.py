import os

# Override env vars before any app modules are imported.
# The .env file sets a placeholder webhook secret which causes
# tests to fail on signature verification.
os.environ["CLERK_WEBHOOK_SECRET"] = ""

import pytest  # noqa: E402


@pytest.fixture
def anyio_backend():
    return "asyncio"
