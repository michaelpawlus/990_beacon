import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";

const mockGetUsageSummary = vi.fn();
const mockApi = {
  searchOrganizations: vi.fn(),
  typeahead: vi.fn(),
  getOrganization: vi.fn(),
  getUsageSummary: mockGetUsageSummary,
};

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
  usePathname: () => "/dashboard/settings",
  useSearchParams: () => new URLSearchParams(),
}));

vi.mock("@clerk/nextjs", () => ({
  useAuth: () => ({ getToken: vi.fn().mockResolvedValue("test-token") }),
}));

vi.mock("@/hooks/use-api", () => ({
  useApi: () => mockApi,
}));

import SettingsPage from "@/app/dashboard/settings/page";

beforeEach(() => {
  mockGetUsageSummary.mockReset();
  mockGetUsageSummary.mockImplementation(() => new Promise(() => {}));
});

afterEach(() => {
  cleanup();
});

describe("SettingsPage", () => {
  it("renders usage section", async () => {
    mockGetUsageSummary.mockResolvedValue({
      searches_today: 5,
      searches_this_month: 42,
      profile_views_today: 3,
      profile_views_this_month: 17,
    });

    render(<SettingsPage />);

    await waitFor(() => {
      expect(screen.getByTestId("usage-cards")).toBeInTheDocument();
    });

    expect(screen.getByTestId("searches-today")).toHaveTextContent("5");
    expect(screen.getByTestId("searches-month")).toHaveTextContent("42");
    expect(screen.getByTestId("views-today")).toHaveTextContent("3");
    expect(screen.getByTestId("views-month")).toHaveTextContent("17");
  });

  it("shows loading state", () => {
    render(<SettingsPage />);
    expect(screen.getByTestId("usage-loading")).toBeInTheDocument();
  });

  it("handles API error gracefully", async () => {
    mockGetUsageSummary.mockRejectedValue(new Error("Network error"));

    render(<SettingsPage />);

    await waitFor(() => {
      expect(
        screen.getByText("Unable to load usage data.")
      ).toBeInTheDocument();
    });
  });
});
