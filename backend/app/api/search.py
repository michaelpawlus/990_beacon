from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.organization import (
    OrganizationSearchResult,
    PaginatedResults,
    SearchFilters,
    TypeaheadResult,
)
from app.services.search import search_organizations, typeahead
from app.services.usage import track_event

router = APIRouter(prefix="/api/v1", tags=["search"])


@router.get("/search", response_model=PaginatedResults[OrganizationSearchResult])
async def search(
    q: str = "",
    state: str | None = None,
    ntee_code: str | None = None,
    min_revenue: int | None = None,
    max_revenue: int | None = None,
    min_assets: int | None = None,
    max_assets: int | None = None,
    filing_year: int | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    filters = SearchFilters(
        q=q,
        state=state,
        ntee_code=ntee_code,
        min_revenue=min_revenue,
        max_revenue=max_revenue,
        min_assets=min_assets,
        max_assets=max_assets,
        filing_year=filing_year,
        page=page,
        page_size=page_size,
    )
    results = await search_organizations(db, filters)
    await track_event(db, current_user.id, "search", {"q": q, "total": results.total})
    return results


@router.get("/search/typeahead", response_model=list[TypeaheadResult])
async def search_typeahead(
    q: str = Query(min_length=2),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await typeahead(db, q)
