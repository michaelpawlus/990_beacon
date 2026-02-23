import "@/test/mocks/clerk";
import { render, screen } from "@testing-library/react";
import LandingPage from "@/app/page";

describe("Landing Page", () => {
  it("renders 990 Beacon heading", () => {
    render(<LandingPage />);
    expect(screen.getByText("990 Beacon")).toBeInTheDocument();
  });

  it("has a sign-up link", () => {
    render(<LandingPage />);
    const signUpLinks = screen.getAllByRole("link", { name: /get started|start free trial/i });
    expect(signUpLinks.length).toBeGreaterThan(0);
    expect(signUpLinks[0]).toHaveAttribute("href", "/sign-up");
  });

  it("has a sign-in link", () => {
    render(<LandingPage />);
    const signInLinks = screen.getAllByRole("link", { name: /sign in/i });
    expect(signInLinks.length).toBeGreaterThan(0);
  });

  it("renders feature descriptions", () => {
    render(<LandingPage />);
    expect(screen.getByText("Search & Explore")).toBeInTheDocument();
    expect(screen.getByText("Financial Health Scores")).toBeInTheDocument();
    expect(screen.getByText("AI Summaries")).toBeInTheDocument();
  });
});
