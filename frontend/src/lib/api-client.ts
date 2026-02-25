import type {
  OrganizationSearchResult,
  PaginatedResults,
  TypeaheadResult,
  OrganizationProfile,
  SearchFilters,
  UsageSummary,
} from "@/lib/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ApiUser {
  id: string;
  clerk_id: string;
  email: string;
  full_name: string | null;
  plan_tier: string;
  created_at: string;
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export function createApiClient(token?: string) {
  async function request<T>(path: string, options?: RequestInit): Promise<T> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options?.headers as Record<string, string>),
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new ApiError(response.status, response.statusText);
    }

    return response.json();
  }

  return {
    getMe: () => request<ApiUser>("/api/v1/me"),
    getHealth: () =>
      request<{ status: string; db: string; version: string }>("/health"),
    searchOrganizations: (filters: SearchFilters) => {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== "") {
          params.set(key, String(value));
        }
      });
      return request<PaginatedResults<OrganizationSearchResult>>(
        `/api/v1/search?${params.toString()}`
      );
    },
    typeahead: (q: string) =>
      request<TypeaheadResult[]>(
        `/api/v1/search/typeahead?q=${encodeURIComponent(q)}`
      ),
    getOrganization: (id: string) =>
      request<OrganizationProfile>(`/api/v1/organizations/${id}`),
    getUsageSummary: () => request<UsageSummary>("/api/v1/usage/summary"),
  };
}
