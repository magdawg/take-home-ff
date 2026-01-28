import type { Metadata } from "next";
import { InsightsDisplay } from "@/components/insights-display";

export const metadata: Metadata = {
  title: "Insights | Dashboard",
  description: "Portfolio insights and metrics",
};

export default function InsightsPage() {
  return (
    <div>
      <h2>Portfolio Insights</h2>
      <p>Key metrics for your investment portfolio:</p>
      <InsightsDisplay />
    </div>
  );
}
