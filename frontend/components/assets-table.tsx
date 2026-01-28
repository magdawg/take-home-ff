"use client";

import React, { useEffect, useState, useCallback, useMemo } from "react";
import { Asset, getAssets } from "@/api";
import styles from "./assets-table.module.css";

type SortColumn = "id" | "nominal_value" | "due_date" | "status";
type SortDirection = "asc" | "desc";

interface TableState {
  sortColumn: SortColumn;
  sortDirection: SortDirection;
  filterStatus: string;
}

export function AssetsTable() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tableState, setTableState] = useState<TableState>({
    sortColumn: "id",
    sortDirection: "asc",
    filterStatus: "all",
  });

  useEffect(() => {
    fetchAssets();
  }, []);

  const fetchAssets = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getAssets();
      setAssets(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch assets");
    } finally {
      setLoading(false);
    }
  }, []);

  const handleSort = useCallback((column: SortColumn) => {
    setTableState((prev) => ({
      ...prev,
      sortColumn: column,
      sortDirection:
        prev.sortColumn === column && prev.sortDirection === "asc"
          ? "desc"
          : "asc",
    }));
  }, []);

  const handleFilterChange = useCallback((e: React.ChangeEvent<HTMLSelectElement>) => {
    setTableState((prev) => ({
      ...prev,
      filterStatus: e.target.value,
    }));
  }, []);

  const filteredAssets = useMemo(() => {
    return assets.filter(
      (asset) =>
        tableState.filterStatus === "all" || asset.status === tableState.filterStatus
    );
  }, [assets, tableState.filterStatus]);

  const sortedAssets = useMemo(() => {
    return [...filteredAssets].sort((a, b) => {
      const column = tableState.sortColumn;
      const direction = tableState.sortDirection === "asc" ? 1 : -1;

      let aValue = a[column];
      let bValue = b[column];

      if (typeof aValue === "string") {
        return direction * aValue.localeCompare(String(bValue));
      }

      return direction * (Number(aValue) - Number(bValue));
    });
  }, [filteredAssets, tableState.sortColumn, tableState.sortDirection]);

  if (loading) {
    return <div className={styles.container}>Loading assets...</div>;
  }

  if (error) {
    return <div className={styles.error}>Error: {error}</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.controls}>
        <label htmlFor="status-filter">Filter by Status:</label>
        <select
          id="status-filter"
          value={tableState.filterStatus}
          onChange={handleFilterChange}
        >
          <option value="all">All</option>
          <option value="active">Active</option>
          <option value="defaulted">Defaulted</option>
        </select>
      </div>

      <table className={styles.table}>
        <thead>
          <tr>
            <th onClick={() => handleSort("id")}>
              ID {tableState.sortColumn === "id" && (tableState.sortDirection === "asc" ? "▲" : "▼")}
            </th>
            <th onClick={() => handleSort("nominal_value")}>
              Nominal Value {tableState.sortColumn === "nominal_value" && (tableState.sortDirection === "asc" ? "▲" : "▼")}
            </th>
            <th onClick={() => handleSort("due_date")}>
              Due Date {tableState.sortColumn === "due_date" && (tableState.sortDirection === "asc" ? "▲" : "▼")}
            </th>
            <th onClick={() => handleSort("status")}>
              Status {tableState.sortColumn === "status" && (tableState.sortDirection === "asc" ? "▲" : "▼")}
            </th>
          </tr>
        </thead>
        <tbody>
          {sortedAssets.length === 0 ? (
            <tr>
              <td colSpan={4} className={styles.empty}>
                No assets found
              </td>
            </tr>
          ) : (
            sortedAssets.map((asset) => (
              <tr key={asset.id}>
                <td>{asset.id}</td>
                <td>${asset.nominal_value.toFixed(2)}</td>
                <td>{asset.due_date}</td>
                <td className={styles[asset.status]}>{asset.status}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
