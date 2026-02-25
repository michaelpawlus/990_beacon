"""Usage event tracking service."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analytics import UsageEvent


async def track_event(
    db: AsyncSession,
    user_id: uuid.UUID,
    event_type: str,
    metadata: dict | None = None,
) -> None:
    """Insert a usage event row."""
    event = UsageEvent(
        user_id=user_id,
        event_type=event_type,
        metadata_=metadata,
    )
    db.add(event)
    await db.flush()
