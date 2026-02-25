"""Usage tracking API endpoints."""

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.analytics import UsageEvent
from app.models.user import User
from app.schemas.usage import UsageSummary

router = APIRouter(prefix="/api/v1", tags=["usage"])


@router.get("/usage/summary", response_model=UsageSummary)
async def get_usage_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()
    month_start = today.replace(day=1)

    async def count_events(event_type: str, since: date) -> int:
        result = await db.execute(
            select(func.count())
            .select_from(UsageEvent)
            .where(
                UsageEvent.user_id == current_user.id,
                UsageEvent.event_type == event_type,
                func.date(UsageEvent.created_at) >= since,
            )
        )
        return result.scalar() or 0

    return UsageSummary(
        searches_today=await count_events("search", today),
        searches_this_month=await count_events("search", month_start),
        profile_views_today=await count_events("profile_view", today),
        profile_views_this_month=await count_events("profile_view", month_start),
    )
