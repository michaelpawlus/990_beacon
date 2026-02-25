export interface OrganizationSearchResult {
  id: string;
  ein: string;
  name: string;
  city: string | null;
  state: string | null;
  ntee_code: string | null;
  latest_revenue: number | null;
  latest_expenses: number | null;
  latest_net_assets: number | null;
  latest_tax_year: number | null;
}

export interface PaginatedResults<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface TypeaheadResult {
  id: string;
  ein: string;
  name: string;
  city: string | null;
  state: string | null;
}

export interface SearchFilters {
  q?: string;
  state?: string;
  ntee_code?: string;
  min_revenue?: number;
  max_revenue?: number;
  min_assets?: number;
  max_assets?: number;
  filing_year?: number;
  page?: number;
  page_size?: number;
}

export interface FilingPerson {
  id: string;
  name: string;
  title: string | null;
  compensation: number | null;
  is_officer: boolean;
  is_director: boolean;
  is_key_employee: boolean;
  is_highest_compensated: boolean;
}

export interface FilingGrant {
  id: string;
  recipient_name: string;
  recipient_ein: string | null;
  recipient_city: string | null;
  recipient_state: string | null;
  amount: number | null;
  purpose: string | null;
}

export interface Filing {
  id: string;
  object_id: string;
  tax_year: number;
  filing_type: string;
  filing_date: string | null;
  total_revenue: number | null;
  total_expenses: number | null;
  net_assets: number | null;
  contributions_and_grants: number | null;
  program_service_revenue: number | null;
  investment_income: number | null;
  program_expenses: number | null;
  management_expenses: number | null;
  fundraising_expenses: number | null;
  num_employees: number | null;
  num_volunteers: number | null;
  mission_description: string | null;
  raw_xml_url: string | null;
  people: FilingPerson[];
  grants: FilingGrant[];
}

export interface ComputedMetrics {
  program_expense_ratio: number | null;
  fundraising_efficiency: number | null;
  revenue_growth_rate: number | null;
}

export interface OrganizationProfile {
  id: string;
  ein: string;
  name: string;
  city: string | null;
  state: string | null;
  ntee_code: string | null;
  ruling_date: string | null;
  filings: Filing[];
  metrics: ComputedMetrics;
}

export interface UsageSummary {
  searches_today: number;
  searches_this_month: number;
  profile_views_today: number;
  profile_views_this_month: number;
}
