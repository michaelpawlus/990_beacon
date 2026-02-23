import "@/test/mocks/clerk";
import { render, screen } from "@testing-library/react";
import DashboardPage from "@/app/dashboard/page";

describe("Dashboard Page", () => {
  it("renders welcome text", () => {
    render(<DashboardPage />);
    expect(screen.getByText("Welcome to 990 Beacon")).toBeInTheDocument();
  });

  it("renders quick action cards", () => {
    render(<DashboardPage />);
    expect(screen.getByText("Search Organizations")).toBeInTheDocument();
    expect(screen.getByText("Watchlists")).toBeInTheDocument();
    expect(screen.getByText("Settings")).toBeInTheDocument();
  });
});
