/**
 * collectMakefileHealth.ts
 * ------------------------
 * Collector wrapper for Makefile health.
 * Normalizes the backend response into the standard
 * RepoHealth collector shape.
 */

import { fetchMakefileHealth } from "../services/makefileHealth.service";

export async function collectMakefileHealth() {
  try {
    const result = await fetchMakefileHealth();

    return {
      ok: result.ok,
      score: result.score,
      detail: result.detail,
    };
  } catch (err) {
    return {
      ok: false,
      score: 0,
      detail: "Unable to retrieve Makefile health",
    };
  }
}
