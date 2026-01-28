"use client";

import React, { useEffect, useState } from "react";
import { Insight, getInsights } from "@/api";
import styles from "./insights-display.module.css";

export function InsightsDisplay() {
  const [insights, setInsights] = useState<Insight[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchInsights();
  }, []);

  async function fetchInsights() {
    try {
      setLoading(true);
      const data = await getInsights();
      setInsights(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch insights");
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div className={styles.container}>Loading insights...</div>;
  }

  if (error) {
    return <div className={styles.error}>Error: {error}</div>;
  }

  const insightsByName = insights.reduce(
    (acc, insight) => {
      acc[insight.name] = insight.value;
      return acc;
    },
    {} as Record<string, number>
  );

  return (
    <div className={styles.container}>
      <div className={styles.grid}>
        {Object.entries(insightsByName).map(([name, value]) => (
          <div key={name} className={styles.card}>
            <div className={styles.label}>{formatLabel(name)}</div>
            <div className={styles.value}>{formatValue(name, value)}</div>
          </div>
        ))}
      </div>

      {insights.length === 0 && (
        <div className={styles.empty}>No insights available. Add assets first.</div>
      )}
    </div>
  );
}

function formatLabel(name: string): string {
  return name
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function formatValue(name: string, value: number): string {
  if (name.includes("interest_rate") || name.includes("percentage")) {
    return `${(value * 100).toFixed(2)}%`;
  }
  if (name.includes("value") || name.includes("nominal")) {
    return `$${value.toFixed(2)}`;
  }
  return value.toFixed(2);
}
