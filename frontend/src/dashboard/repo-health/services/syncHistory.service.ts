/**
 * syncHistory.service.ts
 * ----------------------
 * Fetches the list of repo health snapshots from the backend.
 */

export async function fetchSyncHistory() {
  const res = await fetch("/api/repo/sync-history");

  if (!res.ok) {
    throw new Error("Failed to load sync history");
  }

  return res.json();
}
