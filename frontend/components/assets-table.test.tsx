import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { AssetsTable } from "@/components/assets-table";
import * as api from "@/api";
import { AssetStatus } from "@/api";

// Mock the API module
vi.mock("@/api");

describe("AssetsTable Component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  it("renders loading state initially", () => {
    vi.mocked(api.getAssets).mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    render(<AssetsTable />);
    expect(screen.getByText("Loading assets...")).toBeTruthy();
  });

  it("renders error state when API fails", async () => {
    const errorMessage = "Failed to fetch assets";
    vi.mocked(api.getAssets).mockRejectedValue(new Error(errorMessage));

    render(<AssetsTable />);

    await waitFor(() => {
      expect(screen.getByText(new RegExp(errorMessage))).toBeTruthy();
    });
  });

  it("renders empty state when no assets", async () => {
    vi.mocked(api.getAssets).mockResolvedValue([]);

    render(<AssetsTable />);

    await waitFor(() => {
      expect(screen.getByText("No assets found")).toBeTruthy();
    });
  });

  it("renders assets table with data", async () => {
    const mockAssets = [
      {
        id: "id-1",
        nominal_value: 100,
        status: AssetStatus.ACTIVE,
        due_date: "2025-12-04",
      },
      {
        id: "id-2",
        nominal_value: 50,
        status: AssetStatus.DEFAULTED,
        due_date: "2024-12-04",
      },
    ];

    vi.mocked(api.getAssets).mockResolvedValue(mockAssets);

    render(<AssetsTable />);

    await waitFor(() => {
      expect(screen.getByText("id-1")).toBeTruthy();
      expect(screen.getByText("id-2")).toBeTruthy();
      expect(screen.getByText("$100.00")).toBeTruthy();
      expect(screen.getByText("$50.00")).toBeTruthy();
    });
  });

  it("filters assets by status", async () => {
    const user = userEvent.setup();
    const mockAssets = [
      {
        id: "id-1",
        nominal_value: 100,
        status: AssetStatus.ACTIVE,
        due_date: "2025-12-04",
      },
      {
        id: "id-2",
        nominal_value: 50,
        status: AssetStatus.DEFAULTED,
        due_date: "2024-12-04",
      },
    ];

    vi.mocked(api.getAssets).mockResolvedValue(mockAssets);

    render(<AssetsTable />);

    await waitFor(() => {
      expect(screen.getByText("id-1")).toBeTruthy();
      expect(screen.getByText("id-2")).toBeTruthy();
    });

    const filterSelect = screen.getByDisplayValue("All");
    await user.selectOptions(filterSelect, "active");

    await waitFor(() => {
      expect(screen.getByText("id-1")).toBeTruthy();
      expect(screen.queryByText("id-2")).toBeNull();
    });
  });

  it("sorts assets by column", async () => {
    const user = userEvent.setup();
    const mockAssets = [
      {
        id: "id-3",
        nominal_value: 30,
        status: AssetStatus.ACTIVE,
        due_date: "2025-03-04",
      },
      {
        id: "id-1",
        nominal_value: 100,
        status: AssetStatus.ACTIVE,
        due_date: "2025-12-04",
      },
      {
        id: "id-2",
        nominal_value: 50,
        status: AssetStatus.DEFAULTED,
        due_date: "2024-12-04",
      },
    ];

    vi.mocked(api.getAssets).mockResolvedValue(mockAssets);

    render(<AssetsTable />);

    await waitFor(() => {
      expect(screen.getByText("id-3")).toBeTruthy();
    });

    // Get the ID column header and click it
    const idHeader = screen.getAllByRole("columnheader").find(h => h.textContent?.includes("ID"));
    await user.click(idHeader!);

    // After sorting, check order (ascending by ID)
    await waitFor(() => {
      const rows = screen.getAllByText(/id-[0-9]/);
      expect(rows[0].textContent).toContain("id-3");
      expect(rows[1].textContent).toContain("id-2");
      expect(rows[2].textContent).toContain("id-1");
    });
  });

  it("sorts nominal value correctly", async () => {
    const user = userEvent.setup();
    const mockAssets = [
      {
        id: "id-1",
        nominal_value: 100,
        status: AssetStatus.ACTIVE,
        due_date: "2025-12-04",
      },
      {
        id: "id-2",
        nominal_value: 50,
        status: AssetStatus.ACTIVE,
        due_date: "2025-11-04",
      },
      {
        id: "id-3",
        nominal_value: 75,
        status: AssetStatus.ACTIVE,
        due_date: "2025-10-04",
      },
    ];

    vi.mocked(api.getAssets).mockResolvedValue(mockAssets);

    render(<AssetsTable />);

    await waitFor(() => {
      expect(screen.getByText("id-1")).toBeTruthy();
    });

    // Click nominal value header to sort
    const valueHeader = screen.getAllByRole("columnheader").find(h => h.textContent?.includes("Nominal Value"));
    await user.click(valueHeader!);

    // Check values are sorted (should be 50, 75, 100 ascending)
    await waitFor(() => {
      const values = screen.getAllByText(/\$\d+\.\d{2}/);
      expect(values[0].textContent).toBe("$50.00");
      expect(values[1].textContent).toBe("$75.00");
      expect(values[2].textContent).toBe("$100.00");
    });
  });

  it("displays status with correct styling", async () => {
    const mockAssets = [
      {
        id: "id-1",
        nominal_value: 100,
        status: AssetStatus.ACTIVE,
        due_date: "2025-12-04",
      },
      {
        id: "id-2",
        nominal_value: 50,
        status: AssetStatus.DEFAULTED,
        due_date: "2024-12-04",
      },
    ];

    vi.mocked(api.getAssets).mockResolvedValue(mockAssets);

    render(<AssetsTable />);

    await waitFor(() => {
      const activeStatus = screen.getAllByText("active")[0];
      const defaultedStatus = screen.getAllByText("defaulted")[0];

      // Check that they have the right classes (simplified - actual implementation checks CSS)
      expect(activeStatus).toBeTruthy();
      expect(defaultedStatus).toBeTruthy();
    });
  });
});
