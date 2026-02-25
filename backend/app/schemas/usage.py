"""Usage event schemas."""

from pydantic import BaseModel


class UsageSummary(BaseModel):
    searches_today: int = 0
    searches_this_month: int = 0
    profile_views_today: int = 0
    profile_views_this_month: int = 0
