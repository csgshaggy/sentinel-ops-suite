/**
 * collectSyncHistory.ts
 * ---------------------
 * Collector for sync history health.
 * Updated for Node 24 + ts-node ESM rules:
 * - Explicit .ts extension
 * - Normalized RepoHealth collector shape
 * - Deterministic scoring and error handling
 */

import { fetchSyncHistory } from "../services/syncHistory.service.ts";

export async function collectSyncHistory() {
  try {
    const result = await fetchSyncHistory();

    return {
      ok: result.ok,
      score: result.score ?? 0,
      detail: result.detail ?? {},
    };
  } catch (err) {
    return {
      ok: false,
      score: 0,
      detail: {},
    };
  }
}
