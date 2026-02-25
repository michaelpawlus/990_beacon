import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import SearchPage from "@/app/dashboard/search/page";

const mockPush = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockPush }),
  usePathname: () => "/dashboard/search",
  useSearchParams: () => new URLSearchParams(),
  useParams: () => ({}),
}));

const mockSearchOrganizations = vi.fn();
const mockTypeahead = vi.fn();
const mockApi = {
  searchOrganizations: mockSearchOrganizations,
  typeahead: mockTypeahead,
  getOrganization: vi.fn(),
  getUsageSummary: vi.fn(),
};

vi.mock("@clerk/nextjs", () => ({
  useAuth: () => ({ getToken: vi.fn().mockResolvedValue("test-token") }),
}));

vi.mock("@/hooks/use-api", () => ({
  useApi: () => mockApi,
}));

beforeEach(() => {
  mockSearchOrganizations.mockReset();
  mockTypeahead.mockReset();
  mockPush.mockReset();
});

describe("SearchPage", () => {
  it("renders search bar and filter area", () => {
    render(<SearchPage />);
    expect(screen.getByTestId("search-input")).toBeInTheDocument();
    expect(screen.getByTestId("filter-panel")).toBeInTheDocument();
  });

  it("shows empty state when no query has been entered", () => {
    render(<SearchPage />);
    expect(screen.getByTestId("search-empty-state")).toBeInTheDocument();
    expect(screen.getByText("Search nonprofits")).toBeInTheDocument();
  });

  it("displays results after a search", async () => {
    mockSearchOrganizations.mockResolvedValueOnce({
      items: [
        {
          id: "1",
          ein: "123456789",
          name: "Test Nonprofit",
          city: "Washington",
          state: "DC",
          ntee_code: "P20",
          latest_revenue: 5000000,
          latest_expenses: 4500000,
          latest_net_assets: 2000000,
          latest_tax_year: 2023,
        },
      ],
      total: 1,
      page: 1,
      page_size: 20,
      total_pages: 1,
    });

    render(<SearchPage />);

    const input = screen.getByTestId("search-input");
    fireEvent.change(input, { target: { value: "Test" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByText("Test Nonprofit")).toBeInTheDocument();
    });

    expect(screen.getByText("1 result found")).toBeInTheDocument();
  });

  it("shows loading state during search", async () => {
    let resolveSearch: (value: unknown) => void;
    mockSearchOrganizations.mockReturnValue(
      new Promise((resolve) => {
        resolveSearch = resolve;
      })
    );

    render(<SearchPage />);

    const input = screen.getByTestId("search-input");
    fireEvent.change(input, { target: { value: "Test" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByTestId("search-loading")).toBeInTheDocument();
    });

    resolveSearch!({
      items: [],
      total: 0,
      page: 1,
      page_size: 20,
      total_pages: 0,
    });

    await waitFor(() => {
      expect(screen.queryByTestId("search-loading")).not.toBeInTheDocument();
    });
  });

  it("shows no results state", async () => {
    mockSearchOrganizations.mockResolvedValueOnce({
      items: [],
      total: 0,
      page: 1,
      page_size: 20,
      total_pages: 0,
    });

    render(<SearchPage />);

    const input = screen.getByTestId("search-input");
    fireEvent.change(input, { target: { value: "nonexistent" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByText("No results found")).toBeInTheDocument();
    });
  });
});
