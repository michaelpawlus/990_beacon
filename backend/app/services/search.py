from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Filing, Organization
from app.schemas.organization import (
    OrganizationSearchResult,
    PaginatedResults,
    SearchFilters,
    TypeaheadResult,
)


async def search_organizations(
    db: AsyncSession, filters: SearchFilters
) -> PaginatedResults[OrganizationSearchResult]:
    """Full search with filters, pagination, and latest filing data."""
    # Subquery for the latest filing per organization
    latest_filing_sq = (
        select(
            Filing.organization_id,
            Filing.total_revenue,
            Filing.total_expenses,
            Filing.net_assets,
            Filing.tax_year,
            func.row_number()
            .over(
                partition_by=Filing.organization_id,
                order_by=Filing.tax_year.desc(),
            )
            .label("rn"),
        )
    ).subquery()

    # Main query: Organization LEFT JOIN latest filing (rn == 1)
    query = select(
        Organization.id,
        Organization.ein,
        Organization.name,
        Organization.city,
        Organization.state,
        Organization.ntee_code,
        latest_filing_sq.c.total_revenue.label("latest_revenue"),
        latest_filing_sq.c.total_expenses.label("latest_expenses"),
        latest_filing_sq.c.net_assets.label("latest_net_assets"),
        latest_filing_sq.c.tax_year.label("latest_tax_year"),
    ).outerjoin(
        latest_filing_sq,
        and_(
            latest_filing_sq.c.organization_id == Organization.id,
            latest_filing_sq.c.rn == 1,
        ),
    )

    # Build filter conditions
    conditions = []
    if filters.q:
        conditions.append(Organization.name.op("%")(filters.q))
    if filters.state:
        conditions.append(Organization.state == filters.state)
    if filters.ntee_code:
        conditions.append(Organization.ntee_code == filters.ntee_code)
    if filters.min_revenue is not None:
        conditions.append(latest_filing_sq.c.total_revenue >= filters.min_revenue)
    if filters.max_revenue is not None:
        conditions.append(latest_filing_sq.c.total_revenue <= filters.max_revenue)
    if filters.min_assets is not None:
        conditions.append(latest_filing_sq.c.net_assets >= filters.min_assets)
    if filters.max_assets is not None:
        conditions.append(latest_filing_sq.c.net_assets <= filters.max_assets)
    if filters.filing_year is not None:
        conditions.append(latest_filing_sq.c.tax_year == filters.filing_year)

    if conditions:
        query = query.where(and_(*conditions))

    # Order by similarity when searching, otherwise alphabetical
    if filters.q:
        query = query.order_by(
            func.similarity(Organization.name, filters.q).desc()
        )
    else:
        query = query.order_by(Organization.name)

    # Count total results
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Paginate
    offset = (filters.page - 1) * filters.page_size
    query = query.offset(offset).limit(filters.page_size)

    result = await db.execute(query)
    rows = result.all()

    items = [
        OrganizationSearchResult(
            id=row.id,
            ein=row.ein,
            name=row.name,
            city=row.city,
            state=row.state,
            ntee_code=row.ntee_code,
            latest_revenue=row.latest_revenue,
            latest_expenses=row.latest_expenses,
            latest_net_assets=row.latest_net_assets,
            latest_tax_year=row.latest_tax_year,
        )
        for row in rows
    ]

    total_pages = (total + filters.page_size - 1) // filters.page_size

    return PaginatedResults(
        items=items,
        total=total,
        page=filters.page,
        page_size=filters.page_size,
        total_pages=total_pages,
    )


async def typeahead(
    db: AsyncSession, q: str, limit: int = 10
) -> list[TypeaheadResult]:
    """Fast typeahead search on organization names only."""
    if len(q) < 2:
        return []

    query = (
        select(Organization)
        .where(Organization.name.op("%")(q))
        .order_by(func.similarity(Organization.name, q).desc())
        .limit(limit)
    )

    result = await db.execute(query)
    orgs = result.scalars().all()

    return [TypeaheadResult.model_validate(org) for org in orgs]
