/**
 * collectMakefileHealth.ts
 * ------------------------
 * Collector for Makefile health.
 * Updated for Node 24 + ts-node ESM rules:
 * - Explicit .ts extension
 * - Normalized RepoHealth collector shape
 * - Deterministic scoring and error handling
 */

import { fetchMakefileHealth } from "../services/makefileHealth.service.ts";

export async function collectMakefileHealth() {
  try {
    const result = await fetchMakefileHealth();

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
