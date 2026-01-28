export enum AssetStatus {
  ACTIVE = "active",
  DEFAULTED = "defaulted",
}

export interface Asset {
  id: string;
  nominal_value: number;
  status: AssetStatus;
  due_date: string;
}

export interface Insight {
  id: string;
  name: string;
  value: number;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function getAssets(): Promise<Asset[]> {
  const response = await fetch(`${API_BASE_URL}/asset`);
  if (!response.ok) {
    throw new Error(`Failed to fetch assets: ${response.statusText}`);
  }
  return response.json();
}

export async function getInsights(): Promise<Insight[]> {
  const response = await fetch(`${API_BASE_URL}/insights`);
  if (!response.ok) {
    throw new Error(`Failed to fetch insights: ${response.statusText}`);
  }
  return response.json();
}

export async function createAssets(assets: Array<{
  id: string;
  nominal_value: number;
  due_date: string;
  interest_rate: number;
}>): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/asset`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(assets),
  });
  if (!response.ok) {
    throw new Error(`Failed to create assets: ${response.statusText}`);
  }
  return response.json();
}
