from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: UUID
    clerk_id: str
    email: str
    full_name: str | None = None
    plan_tier: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ClerkWebhookEvent(BaseModel):
    """Clerk webhook event payload."""
    type: str
    data: dict
