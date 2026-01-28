import { describe, it, expect, vi, beforeEach } from "vitest";
import * as api from "@/api";
import { AssetStatus } from "@/api";

// Mock fetch for API tests
global.fetch = vi.fn();

describe("API Module", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("getAssets", () => {
    it("fetches assets successfully", async () => {
      const mockAssets = [
        {
          id: "id-1",
          nominal_value: 100,
          status: AssetStatus.ACTIVE,
          due_date: "2025-12-04",
        },
      ];

      vi.mocked(fetch).mockResolvedValue({
        ok: true,
        json: async () => mockAssets,
      } as Response);

      const result = await api.getAssets();

      expect(result).toEqual(mockAssets);
      expect(fetch).toHaveBeenCalledWith("http://localhost:8000/asset");
    });

    it("throws error on fetch failure", async () => {
      vi.mocked(fetch).mockResolvedValue({
        ok: false,
        statusText: "Not Found",
      } as Response);

      await expect(api.getAssets()).rejects.toThrow(
        "Failed to fetch assets: Not Found"
      );
    });
  });

  describe("getInsights", () => {
    it("fetches insights successfully", async () => {
      const mockInsights = [
        { id: "insight-1", name: "total_nominal_value", value: 140 },
      ];

      vi.mocked(fetch).mockResolvedValue({
        ok: true,
        json: async () => mockInsights,
      } as Response);

      const result = await api.getInsights();

      expect(result).toEqual(mockInsights);
      expect(fetch).toHaveBeenCalledWith("http://localhost:8000/insights");
    });

    it("throws error on fetch failure", async () => {
      vi.mocked(fetch).mockResolvedValue({
        ok: false,
        statusText: "Server Error",
      } as Response);

      await expect(api.getInsights()).rejects.toThrow(
        "Failed to fetch insights: Server Error"
      );
    });
  });

  describe("createAssets", () => {
    it("creates assets successfully", async () => {
      const newAssets = [
        {
          id: "id-1",
          nominal_value: 100,
          due_date: "2025-12-04",
          interest_rate: 0.03,
        },
      ];

      const mockResponse = { message: "Successfully created 1 assets" };

      vi.mocked(fetch).mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      } as Response);

      const result = await api.createAssets(newAssets);

      expect(result).toEqual(mockResponse);
      expect(fetch).toHaveBeenCalledWith("http://localhost:8000/asset", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newAssets),
      });
    });

    it("throws error on creation failure", async () => {
      const newAssets = [
        {
          id: "id-1",
          nominal_value: -100,
          due_date: "2025-12-04",
          interest_rate: 0.03,
        },
      ];

      vi.mocked(fetch).mockResolvedValue({
        ok: false,
        statusText: "Bad Request",
      } as Response);

      await expect(api.createAssets(newAssets)).rejects.toThrow(
        "Failed to create assets: Bad Request"
      );
    });
  });
});
