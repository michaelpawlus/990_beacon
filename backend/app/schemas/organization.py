from uuid import UUID

from pydantic import BaseModel


class OrganizationSearchResult(BaseModel):
    id: UUID
    ein: str
    name: str
    city: str | None = None
    state: str | None = None
    ntee_code: str | None = None
    latest_revenue: int | None = None
    latest_expenses: int | None = None
    latest_net_assets: int | None = None
    latest_tax_year: int | None = None

    model_config = {"from_attributes": True}


class SearchFilters(BaseModel):
    q: str = ""
    state: str | None = None
    ntee_code: str | None = None
    min_revenue: int | None = None
    max_revenue: int | None = None
    min_assets: int | None = None
    max_assets: int | None = None
    filing_year: int | None = None
    page: int = 1
    page_size: int = 20


class PaginatedResults[T](BaseModel):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int


class TypeaheadResult(BaseModel):
    id: UUID
    ein: str
    name: str
    city: str | None = None
    state: str | None = None

    model_config = {"from_attributes": True}
