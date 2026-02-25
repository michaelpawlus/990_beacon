from datetime import date
from uuid import UUID

from pydantic import BaseModel


class FilingPersonResponse(BaseModel):
    id: UUID
    name: str
    title: str | None = None
    compensation: int | None = None
    is_officer: bool = False
    is_director: bool = False
    is_key_employee: bool = False
    is_highest_compensated: bool = False

    model_config = {"from_attributes": True}


class FilingGrantResponse(BaseModel):
    id: UUID
    recipient_name: str
    recipient_ein: str | None = None
    recipient_city: str | None = None
    recipient_state: str | None = None
    amount: int | None = None
    purpose: str | None = None

    model_config = {"from_attributes": True}


class FilingResponse(BaseModel):
    id: UUID
    object_id: str
    tax_year: int
    filing_type: str
    filing_date: date | None = None
    total_revenue: int | None = None
    total_expenses: int | None = None
    net_assets: int | None = None
    contributions_and_grants: int | None = None
    program_service_revenue: int | None = None
    investment_income: int | None = None
    program_expenses: int | None = None
    management_expenses: int | None = None
    fundraising_expenses: int | None = None
    num_employees: int | None = None
    num_volunteers: int | None = None
    mission_description: str | None = None
    raw_xml_url: str | None = None
    people: list[FilingPersonResponse] = []
    grants: list[FilingGrantResponse] = []

    model_config = {"from_attributes": True}


class ComputedMetrics(BaseModel):
    program_expense_ratio: float | None = None
    fundraising_efficiency: float | None = None
    revenue_growth_rate: float | None = None


class OrganizationProfile(BaseModel):
    id: UUID
    ein: str
    name: str
    city: str | None = None
    state: str | None = None
    ntee_code: str | None = None
    ruling_date: date | None = None
    filings: list[FilingResponse] = []
    metrics: ComputedMetrics = ComputedMetrics()

    model_config = {"from_attributes": True}
