import { describe, it, expect, vi, beforeEach } from "vitest";
import { createApiClient, ApiError } from "@/lib/api-client";

const mockFetch = vi.fn();
global.fetch = mockFetch;

beforeEach(() => {
  mockFetch.mockReset();
});

describe("createApiClient", () => {
  it("attaches auth header when token provided", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ id: "1", email: "test@test.com" }),
    });

    const client = createApiClient("test-token");
    await client.getMe();

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/v1/me"),
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: "Bearer test-token",
        }),
      })
    );
  });

  it("throws ApiError on 401", async () => {
    mockFetch.mockResolvedValue({
      ok: false,
      status: 401,
      statusText: "Unauthorized",
    });

    const client = createApiClient("bad-token");
    await expect(client.getMe()).rejects.toThrow(ApiError);
    await expect(client.getMe()).rejects.toMatchObject({ status: 401 });
  });

  it("throws on network error", async () => {
    mockFetch.mockRejectedValueOnce(new Error("Network error"));

    const client = createApiClient("token");
    await expect(client.getMe()).rejects.toThrow("Network error");
  });
});
