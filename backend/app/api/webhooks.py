import json

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from svix.webhooks import Webhook, WebhookVerificationError

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

router = APIRouter(prefix="/api/v1", tags=["webhooks"])


@router.post("/webhooks/clerk")
async def clerk_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle Clerk webhook events (user.created, user.updated, user.deleted)."""
    body = await request.body()
    headers = dict(request.headers)

    # Verify webhook signature
    if settings.CLERK_WEBHOOK_SECRET:
        try:
            wh = Webhook(settings.CLERK_WEBHOOK_SECRET)
            payload = wh.verify(body, headers)
        except WebhookVerificationError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid webhook signature",
            ) from exc
    else:
        payload = json.loads(body)

    event_type = payload.get("type", "")
    data = payload.get("data", {})

    if event_type == "user.created":
        await _handle_user_created(data, db)
    elif event_type == "user.updated":
        await _handle_user_updated(data, db)
    elif event_type == "user.deleted":
        await _handle_user_deleted(data, db)

    return {"status": "ok"}


async def _handle_user_created(data: dict, db: AsyncSession) -> None:
    clerk_id = data.get("id", "")
    email = _extract_email(data)

    # Idempotent: skip if user already exists
    result = await db.execute(select(User).where(User.clerk_id == clerk_id))
    if result.scalar_one_or_none() is not None:
        return

    user = User(
        clerk_id=clerk_id,
        email=email,
        full_name=_extract_name(data),
    )
    db.add(user)
    await db.commit()


async def _handle_user_updated(data: dict, db: AsyncSession) -> None:
    clerk_id = data.get("id", "")
    result = await db.execute(select(User).where(User.clerk_id == clerk_id))
    user = result.scalar_one_or_none()
    if user is None:
        return

    user.email = _extract_email(data)
    user.full_name = _extract_name(data)
    await db.commit()


async def _handle_user_deleted(data: dict, db: AsyncSession) -> None:
    clerk_id = data.get("id", "")
    result = await db.execute(select(User).where(User.clerk_id == clerk_id))
    user = result.scalar_one_or_none()
    if user is None:
        return

    await db.delete(user)
    await db.commit()


def _extract_email(data: dict) -> str:
    email_addresses = data.get("email_addresses", [])
    if email_addresses:
        return str(email_addresses[0].get("email_address", ""))
    return ""


def _extract_name(data: dict) -> str:
    first = data.get("first_name", "") or ""
    last = data.get("last_name", "") or ""
    return f"{first} {last}".strip()
