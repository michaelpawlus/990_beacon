from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.profile import OrganizationProfile
from app.services.profile import get_organization_by_ein, get_organization_profile
from app.services.usage import track_event

router = APIRouter(prefix="/api/v1", tags=["organizations"])


@router.get("/organizations/by-ein/{ein}", response_model=OrganizationProfile)
async def get_organization_by_ein_endpoint(
    ein: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = await get_organization_by_ein(db, ein)
    if not profile:
        raise HTTPException(status_code=404, detail="Organization not found")
    await track_event(
        db, current_user.id, "profile_view", {"ein": ein, "org_id": str(profile.id)}
    )
    return profile


@router.get("/organizations/{org_id}", response_model=OrganizationProfile)
async def get_organization(
    org_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = await get_organization_profile(db, org_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Organization not found")
    await track_event(
        db, current_user.id, "profile_view", {"org_id": str(org_id)}
    )
    return profile
