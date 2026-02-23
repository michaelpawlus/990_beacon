import "@/test/mocks/clerk";
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import { Sidebar } from "@/components/sidebar";

// Mock next/navigation
vi.mock("next/navigation", () => ({
  usePathname: vi.fn(() => "/dashboard"),
}));

describe("Sidebar", () => {
  it("renders navigation links", () => {
    render(<Sidebar />);
    expect(screen.getByText("Home")).toBeInTheDocument();
    expect(screen.getByText("Search")).toBeInTheDocument();
    expect(screen.getByText("Watchlists")).toBeInTheDocument();
    expect(screen.getByText("Settings")).toBeInTheDocument();
  });

  it("highlights the active link", () => {
    render(<Sidebar />);
    const homeLink = screen.getByText("Home");
    expect(homeLink).toHaveAttribute("data-active", "true");
  });

  it("does not highlight inactive links", () => {
    render(<Sidebar />);
    const searchLink = screen.getByText("Search");
    expect(searchLink).toHaveAttribute("data-active", "false");
  });
});
