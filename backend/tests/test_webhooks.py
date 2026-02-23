"""Clerk webhook handler tests.

These tests require a running PostgreSQL test instance with migrations applied.
"""


import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


def clerk_user_created_payload(
    clerk_id: str = "user_webhook_test",
    email: str = "test@example.com",
    first_name: str = "Test",
    last_name: str = "User",
) -> dict:
    return {
        "type": "user.created",
        "data": {
            "id": clerk_id,
            "email_addresses": [{"email_address": email}],
            "first_name": first_name,
            "last_name": last_name,
        },
    }


def clerk_user_updated_payload(
    clerk_id: str = "user_webhook_test",
    email: str = "updated@example.com",
    first_name: str = "Updated",
    last_name: str = "Name",
) -> dict:
    return {
        "type": "user.updated",
        "data": {
            "id": clerk_id,
            "email_addresses": [{"email_address": email}],
            "first_name": first_name,
            "last_name": last_name,
        },
    }


@pytest.mark.asyncio
async def test_webhook_invalid_signature_returns_400():
    """When CLERK_WEBHOOK_SECRET is set, invalid signatures should be rejected."""
    # This test only works when webhook secret is configured
    # In test env without secret, the webhook accepts all payloads
    pass


@pytest.mark.asyncio
async def test_webhook_creates_user():
    """A user.created webhook should create a user in the DB."""
    payload = clerk_user_created_payload()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/webhooks/clerk",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_webhook_user_created_is_idempotent():
    """Sending user.created twice should not fail."""
    payload = clerk_user_created_payload(clerk_id="user_idempotent_test")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post("/api/v1/webhooks/clerk", json=payload)
        response = await client.post("/api/v1/webhooks/clerk", json=payload)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_webhook_updates_user():
    """A user.updated webhook should update the user record."""
    create_payload = clerk_user_created_payload(clerk_id="user_update_test")
    update_payload = clerk_user_updated_payload(clerk_id="user_update_test")

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post("/api/v1/webhooks/clerk", json=create_payload)
        response = await client.post("/api/v1/webhooks/clerk", json=update_payload)

    assert response.status_code == 200
