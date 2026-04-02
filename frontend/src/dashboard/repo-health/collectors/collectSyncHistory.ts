/**
 * collectSyncHistory.ts
 * ---------------------
 * Normalizes sync history into a dashboard-friendly structure.
 */

import { fetchSyncHistory } from "../services/syncHistory.service";

export async function collectSyncHistory() {
  try {
    const history = await fetchSyncHistory();

    return {
      ok: true,
      entries: history.entries || [],
    };
  } catch {
    return {
      ok: false,
      entries: [],
    };
  }
}
