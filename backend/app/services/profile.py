from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.organization import Filing, Organization
from app.schemas.profile import (
    ComputedMetrics,
    FilingResponse,
    OrganizationProfile,
)


async def get_organization_profile(
    db: AsyncSession, org_id: UUID
) -> OrganizationProfile | None:
    """Get full organization profile with filings, people, grants."""
    query = (
        select(Organization)
        .options(
            selectinload(Organization.filings).selectinload(Filing.people),
            selectinload(Organization.filings).selectinload(Filing.grants),
        )
        .where(Organization.id == org_id)
    )
    result = await db.execute(query)
    org = result.scalar_one_or_none()
    if not org:
        return None

    sorted_filings = sorted(org.filings, key=lambda f: f.tax_year, reverse=True)
    filing_responses = [FilingResponse.model_validate(f) for f in sorted_filings]
    metrics = compute_metrics(sorted_filings)

    return OrganizationProfile(
        id=org.id,
        ein=org.ein,
        name=org.name,
        city=org.city,
        state=org.state,
        ntee_code=org.ntee_code,
        ruling_date=org.ruling_date,
        filings=filing_responses,
        metrics=metrics,
    )


async def get_organization_by_ein(
    db: AsyncSession, ein: str
) -> OrganizationProfile | None:
    """Get organization by EIN."""
    query = (
        select(Organization)
        .options(
            selectinload(Organization.filings).selectinload(Filing.people),
            selectinload(Organization.filings).selectinload(Filing.grants),
        )
        .where(Organization.ein == ein)
    )
    result = await db.execute(query)
    org = result.scalar_one_or_none()
    if not org:
        return None

    sorted_filings = sorted(org.filings, key=lambda f: f.tax_year, reverse=True)
    filing_responses = [FilingResponse.model_validate(f) for f in sorted_filings]
    metrics = compute_metrics(sorted_filings)

    return OrganizationProfile(
        id=org.id,
        ein=org.ein,
        name=org.name,
        city=org.city,
        state=org.state,
        ntee_code=org.ntee_code,
        ruling_date=org.ruling_date,
        filings=filing_responses,
        metrics=metrics,
    )


def compute_metrics(filings: list) -> ComputedMetrics:
    """Calculate financial metrics from filing data."""
    if not filings:
        return ComputedMetrics()

    latest = filings[0]  # Already sorted desc by tax_year

    # Program expense ratio = program_expenses / total_expenses
    program_expense_ratio = None
    if (
        latest.total_expenses
        and latest.total_expenses > 0
        and latest.program_expenses is not None
    ):
        program_expense_ratio = latest.program_expenses / latest.total_expenses

    # Fundraising efficiency = fundraising_expenses / total_expenses
    fundraising_efficiency = None
    if (
        latest.total_expenses
        and latest.total_expenses > 0
        and latest.fundraising_expenses is not None
    ):
        fundraising_efficiency = latest.fundraising_expenses / latest.total_expenses

    # Revenue growth rate = (current - previous) / abs(previous)
    revenue_growth_rate = None
    if len(filings) >= 2:
        current_rev = latest.total_revenue
        previous = filings[1]
        previous_rev = previous.total_revenue
        if current_rev is not None and previous_rev is not None and previous_rev != 0:
            revenue_growth_rate = (current_rev - previous_rev) / abs(previous_rev)

    return ComputedMetrics(
        program_expense_ratio=program_expense_ratio,
        fundraising_efficiency=fundraising_efficiency,
        revenue_growth_rate=revenue_growth_rate,
    )
