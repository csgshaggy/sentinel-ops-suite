// dashboard/src/api/client.ts

import { Plugin, TimingBucket } from "../types";

const BASE_URL = "http://127.0.0.1:5001/api";

// ------------------------------------------------------------
// Fetch all plugins
// ------------------------------------------------------------
export async function fetchPlugins(): Promise<Plugin[]> {
  const res = await fetch(`${BASE_URL}/plugins`);
  if (!res.ok) throw new Error("Failed to fetch plugins");
  return res.json();
}

// ------------------------------------------------------------
// Fetch timing histogram buckets
// ------------------------------------------------------------
export async function fetchTimingBuckets(): Promise<TimingBucket[]> {
  const res = await fetch(`${BASE_URL}/metrics/timing`);
  if (!res.ok) throw new Error("Failed to fetch timing metrics");
  return res.json();
}

// ------------------------------------------------------------
// Fetch logs for a specific plugin
// ------------------------------------------------------------
export async function fetchPluginLogs(pluginId: string): Promise<string[]> {
  const res = await fetch(`${BASE_URL}/plugins/${pluginId}/logs`);
  if (!res.ok) throw new Error("Failed to fetch plugin logs");
  return res.json();
}

// ------------------------------------------------------------
// Fetch Makefile diff
// ------------------------------------------------------------
export async function fetchMakefileDiff(): Promise<{
  diff: string[];
  health: number;
  warning?: string;
}> {
  const res = await fetch(`${BASE_URL}/makefile/diff`);
  if (!res.ok) throw new Error("Failed to fetch Makefile diff");
  return res.json();
}

// ------------------------------------------------------------
// Fetch Makefile health score
// ------------------------------------------------------------
export async function fetchMakefileHealth(): Promise<{
  health: number;
  warning?: string;
}> {
  const res = await fetch(`${BASE_URL}/makefile/health`);
  if (!res.ok) throw new Error("Failed to fetch Makefile health");
  return res.json();
}

// ------------------------------------------------------------
// Fetch full Makefile
// ------------------------------------------------------------
export async function fetchMakefile(): Promise<{
  path: string;
  lines: string[];
}> {
  const res = await fetch(`${BASE_URL}/makefile`);
  if (!res.ok) throw new Error("Failed to fetch Makefile");
  return res.json();
}

// ------------------------------------------------------------
// Fetch reference Makefile
// ------------------------------------------------------------
export async function fetchReferenceMakefile(): Promise<{
  path: string | null;
  lines: string[];
  warning?: string;
}> {
  const res = await fetch(`${BASE_URL}/makefile/reference`);
  if (!res.ok) throw new Error("Failed to fetch reference Makefile");
  return res.json();
}
