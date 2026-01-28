import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { InsightsDisplay } from "@/components/insights-display";
import * as api from "@/api";

// Mock the API module
vi.mock("@/api");

describe("InsightsDisplay Component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  it("renders loading state initially", () => {
    vi.mocked(api.getInsights).mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    render(<InsightsDisplay />);
    expect(screen.getByText("Loading insights...")).toBeTruthy();
  });

  it("renders error state when API fails", async () => {
    const errorMessage = "Failed to fetch insights";
    vi.mocked(api.getInsights).mockRejectedValue(new Error(errorMessage));

    render(<InsightsDisplay />);

    await waitFor(() => {
      expect(screen.getByText(new RegExp(errorMessage))).toBeTruthy();
    });
  });

  it("renders empty state when no insights", async () => {
    vi.mocked(api.getInsights).mockResolvedValue([]);

    render(<InsightsDisplay />);

    await waitFor(() => {
      expect(screen.getByText(/No insights available/)).toBeTruthy();
    });
  });

  it("renders insights cards with data", async () => {
    const mockInsights = [
      { id: "insight-1", name: "total_nominal_value", value: 140 },
      { id: "insight-2", name: "average_interest_rate", value: 0.06 },
    ];

    vi.mocked(api.getInsights).mockResolvedValue(mockInsights);

    render(<InsightsDisplay />);

    await waitFor(() => {
      expect(screen.getByText("Total Nominal Value")).toBeTruthy();
      expect(screen.getByText("$140.00")).toBeTruthy();
      expect(screen.getByText("Average Interest Rate")).toBeTruthy();
      expect(screen.getByText("6.00%")).toBeTruthy();
    });
  });

  it("formats interest rate as percentage", async () => {
    const mockInsights = [
      { id: "insight-1", name: "average_interest_rate", value: 0.05 },
    ];

    vi.mocked(api.getInsights).mockResolvedValue(mockInsights);

    render(<InsightsDisplay />);

    await waitFor(() => {
      expect(screen.getByText("5.00%")).toBeTruthy();
    });
  });

  it("formats nominal value as currency", async () => {
    const mockInsights = [
      { id: "insight-1", name: "total_nominal_value", value: 1234.56 },
    ];

    vi.mocked(api.getInsights).mockResolvedValue(mockInsights);

    render(<InsightsDisplay />);

    await waitFor(() => {
      expect(screen.getByText("$1234.56")).toBeTruthy();
    });
  });

  it("handles multiple insight cards", async () => {
    const mockInsights = [
      { id: "insight-1", name: "total_nominal_value", value: 500 },
      { id: "insight-2", name: "average_interest_rate", value: 0.08 },
      { id: "insight-3", name: "some_other_metric", value: 42 },
    ];

    vi.mocked(api.getInsights).mockResolvedValue(mockInsights);

    render(<InsightsDisplay />);

    await waitFor(() => {
      expect(screen.getByText("Total Nominal Value")).toBeTruthy();
      expect(screen.getByText("Average Interest Rate")).toBeTruthy();
      expect(screen.getByText("Some Other Metric")).toBeTruthy();
      expect(screen.getByText("42.00")).toBeTruthy();
    });
  });

  it("refreshes on component mount", async () => {
    const mockInsights = [
      { id: "insight-1", name: "total_nominal_value", value: 100 },
    ];

    vi.mocked(api.getInsights).mockResolvedValue(mockInsights);

    render(<InsightsDisplay />);

    await waitFor(() => {
      expect(api.getInsights).toHaveBeenCalledTimes(1);
      expect(screen.getByText("$100.00")).toBeTruthy();
    });
  });
});
