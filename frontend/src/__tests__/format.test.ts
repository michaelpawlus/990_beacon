import { describe, it, expect } from "vitest";
import {
  formatCurrency,
  formatPercent,
  formatCompactNumber,
} from "@/lib/format";

describe("formatCurrency", () => {
  it("formats a number as USD", () => {
    expect(formatCurrency(3000000)).toBe("$3,000,000");
  });

  it("handles null", () => {
    expect(formatCurrency(null)).toBe("N/A");
  });

  it("handles undefined", () => {
    expect(formatCurrency(undefined)).toBe("N/A");
  });

  it("handles zero", () => {
    expect(formatCurrency(0)).toBe("$0");
  });

  it("handles negative numbers", () => {
    expect(formatCurrency(-500000)).toBe("-$500,000");
  });
});

describe("formatPercent", () => {
  it("formats a decimal as a percentage", () => {
    expect(formatPercent(0.897)).toBe("89.7%");
  });

  it("handles null", () => {
    expect(formatPercent(null)).toBe("N/A");
  });

  it("handles zero", () => {
    expect(formatPercent(0)).toBe("0.0%");
  });
});

describe("formatCompactNumber", () => {
  it("formats millions compactly", () => {
    expect(formatCompactNumber(1000000)).toBe("1M");
  });

  it("formats billions compactly", () => {
    expect(formatCompactNumber(1500000000)).toBe("1.5B");
  });

  it("handles null", () => {
    expect(formatCompactNumber(null)).toBe("N/A");
  });

  it("handles small numbers", () => {
    expect(formatCompactNumber(500)).toBe("500");
  });
});
