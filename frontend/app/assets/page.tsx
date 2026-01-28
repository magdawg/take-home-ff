import type { Metadata } from "next";
import { AssetsTable } from "@/components/assets-table";

export const metadata: Metadata = {
  title: "Assets | Dashboard",
  description: "View and manage your portfolio assets",
};

export default function AssetsPage() {
  return (
    <div>
      <h2>Portfolio Assets</h2>
      <p>Manage and track your investment assets:</p>
      <AssetsTable />
    </div>
  );
}
