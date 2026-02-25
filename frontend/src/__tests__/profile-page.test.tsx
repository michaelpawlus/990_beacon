import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import type { OrganizationProfile } from "@/lib/types";

const mockPush = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockPush }),
  usePathname: () => "/dashboard/organizations/1",
  useSearchParams: () => new URLSearchParams(),
  useParams: () => ({ id: "1" }),
}));

vi.mock("@clerk/nextjs", () => ({
  useAuth: () => ({ getToken: vi.fn().mockResolvedValue("test-token") }),
}));

const mockGetOrganization = vi.fn();
const mockApi = {
  searchOrganizations: vi.fn(),
  typeahead: vi.fn(),
  getOrganization: mockGetOrganization,
  getUsageSummary: vi.fn(),
};

vi.mock("@/hooks/use-api", () => ({
  useApi: () => mockApi,
}));

// Mock recharts to avoid rendering issues in JSDOM
vi.mock("recharts", () => ({
  LineChart: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="line-chart">{children}</div>
  ),
  Line: () => <div />,
  XAxis: () => <div />,
  YAxis: () => <div />,
  CartesianGrid: () => <div />,
  Tooltip: () => <div />,
  Legend: () => <div />,
  ResponsiveContainer: ({ children }: { children: React.ReactNode }) => (
    <div>{children}</div>
  ),
}));

// Mock radix-ui Tabs to avoid heavy radix dependencies in JSDOM
vi.mock("@/components/ui/tabs", () => ({
  Tabs: ({
    children,
    ...props
  }: {
    children: React.ReactNode;
    defaultValue?: string;
  }) => (
    <div data-testid="tabs" data-value={props.defaultValue}>
      {children}
    </div>
  ),
  TabsList: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="tabs-list">{children}</div>
  ),
  TabsTrigger: ({
    children,
    value,
  }: {
    children: React.ReactNode;
    value: string;
  }) => <button data-value={value}>{children}</button>,
  TabsContent: ({
    children,
  }: {
    children: React.ReactNode;
    value?: string;
    className?: string;
  }) => <div>{children}</div>,
}));

const { default: OrganizationProfilePage } = await import(
  "@/app/dashboard/organizations/[id]/page"
);

const mockOrg: OrganizationProfile = {
  id: "1",
  ein: "123456789",
  name: "American Red Cross",
  city: "Washington",
  state: "DC",
  ntee_code: "P20",
  ruling_date: "1946-01-01",
  filings: [
    {
      id: "f1",
      object_id: "obj_123",
      tax_year: 2023,
      filing_type: "990",
      filing_date: "2024-05-15",
      total_revenue: 3000000000,
      total_expenses: 2900000000,
      net_assets: 1500000000,
      contributions_and_grants: 2500000000,
      program_service_revenue: 300000000,
      investment_income: 100000000,
      program_expenses: 2600000000,
      management_expenses: 200000000,
      fundraising_expenses: 100000000,
      num_employees: 30000,
      num_volunteers: 200000,
      mission_description: "Preventing and alleviating human suffering.",
      raw_xml_url: null,
      people: [
        {
          id: "p1",
          name: "John CEO",
          title: "CEO",
          compensation: 500000,
          is_officer: true,
          is_director: false,
          is_key_employee: false,
          is_highest_compensated: false,
        },
      ],
      grants: [],
    },
  ],
  metrics: {
    program_expense_ratio: 0.897,
    fundraising_efficiency: 0.034,
    revenue_growth_rate: 0.05,
  },
};

beforeEach(() => {
  mockGetOrganization.mockReset();
  // Ensure that any stray effect calls don't throw by defaulting to a pending promise
  mockGetOrganization.mockImplementation(() => new Promise(() => {}));
});

afterEach(() => {
  cleanup();
});

describe("OrganizationProfilePage", () => {
  it("renders profile header with org info", async () => {
    mockGetOrganization.mockResolvedValue(mockOrg);

    render(<OrganizationProfilePage />);

    await waitFor(() => {
      expect(screen.getByTestId("profile-header")).toBeInTheDocument();
    });

    expect(screen.getByText("American Red Cross")).toBeInTheDocument();
    expect(
      screen.getByText(/EIN: 123456789.*Washington, DC/)
    ).toBeInTheDocument();
  });

  it("renders financial overview", async () => {
    mockGetOrganization.mockResolvedValue(mockOrg);

    render(<OrganizationProfilePage />);

    await waitFor(() => {
      expect(screen.getByTestId("financial-overview")).toBeInTheDocument();
    });

    expect(screen.getByText("$3,000,000,000")).toBeInTheDocument();
  });

  it("shows loading state", () => {
    render(<OrganizationProfilePage />);

    expect(screen.getByTestId("profile-loading")).toBeInTheDocument();
  });

  it("shows error state on 404", async () => {
    mockGetOrganization.mockRejectedValue({ status: 404 });

    render(<OrganizationProfilePage />);

    await waitFor(() => {
      expect(screen.getByTestId("profile-error")).toBeInTheDocument();
    });

    expect(screen.getByText("Organization not found.")).toBeInTheDocument();
  });

  it("shows N/A for missing metric values", async () => {
    const orgWithNullMetrics = {
      ...mockOrg,
      metrics: {
        program_expense_ratio: null,
        fundraising_efficiency: null,
        revenue_growth_rate: null,
      },
    };
    mockGetOrganization.mockResolvedValue(orgWithNullMetrics);

    render(<OrganizationProfilePage />);

    await waitFor(() => {
      expect(screen.getByTestId("metrics-cards")).toBeInTheDocument();
    });

    const naElements = screen.getAllByText("N/A");
    expect(naElements.length).toBeGreaterThanOrEqual(3);
  });

  it("renders mission description", async () => {
    mockGetOrganization.mockResolvedValue(mockOrg);

    render(<OrganizationProfilePage />);

    await waitFor(() => {
      expect(
        screen.getByText("Preventing and alleviating human suffering.")
      ).toBeInTheDocument();
    });
  });
});
