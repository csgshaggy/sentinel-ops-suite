import { Plugin, TimingBucket } from "../types";

const BASE_URL = "http://127.0.0.1:5001";

export async function fetchPlugins(): Promise<Plugin[]> {
  const res = await fetch(`${BASE_URL}/api/plugins`);
  if (!res.ok) throw new Error("Failed to fetch plugins");
  return res.json();
}

export async function fetchTimingBuckets(): Promise<TimingBucket[]> {
  const res = await fetch(`${BASE_URL}/api/metrics/timing`);
  if (!res.ok) throw new Error("Failed to fetch timing metrics");
  return res.json();
}
