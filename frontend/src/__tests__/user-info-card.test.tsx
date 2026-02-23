import "@/test/mocks/clerk";
import { render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";
import { UserInfoCard } from "@/components/user-info-card";

// Mock the useApi hook
const mockGetMe = vi.fn();

vi.mock("@/hooks/use-api", () => ({
  useApi: () => ({
    getMe: mockGetMe,
  }),
}));

describe("UserInfoCard", () => {
  it("shows loading state", () => {
    mockGetMe.mockReturnValue(new Promise(() => {})); // Never resolves
    render(<UserInfoCard />);
    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("shows user data after loading", async () => {
    mockGetMe.mockResolvedValueOnce({
      id: "1",
      clerk_id: "clerk_1",
      email: "test@example.com",
      full_name: "Test User",
      plan_tier: "free",
      created_at: "2024-01-01T00:00:00Z",
    });

    render(<UserInfoCard />);

    await waitFor(() => {
      expect(screen.getByText("Test User")).toBeInTheDocument();
    });
    expect(screen.getByText("test@example.com")).toBeInTheDocument();
  });

  it("shows error state with retry button", async () => {
    mockGetMe.mockRejectedValueOnce(new Error("Failed to fetch"));

    render(<UserInfoCard />);

    await waitFor(() => {
      expect(screen.getByText("Failed to fetch")).toBeInTheDocument();
    });
    expect(screen.getByRole("button", { name: "Retry" })).toBeInTheDocument();
  });
});
