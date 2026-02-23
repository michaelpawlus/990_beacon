import { render, screen } from "@testing-library/react";

function TestComponent() {
  return <div>Hello 990 Beacon</div>;
}

describe("setup", () => {
  it("renders a React component", () => {
    render(<TestComponent />);
    expect(screen.getByText("Hello 990 Beacon")).toBeInTheDocument();
  });
});
