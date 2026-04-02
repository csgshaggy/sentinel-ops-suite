/**
 * collectStructureHealth.ts
 * -------------------------
 * Collector for repository structure health.
 * This version matches all architecture changes from April 2, 2026:
 * - ESM-safe explicit .ts imports
 * - Normalized RepoHealth collector shape
 * - Deterministic scoring
 * - Compatible with post-sync snapshot pipeline
 */

export async function collectStructureHealth() {
  try {
    const res = await fetch("/api/structure/health");

    if (!res.ok) {
      return {
        ok: false,
        score: 0,
        detail: {},
      };
    }

    const data = await res.json();

    return {
      ok: true,
      score: data.score ?? 0,
      detail: data,
    };
  } catch (err) {
    return {
      ok: false,
      score: 0,
      detail: {},
    };
  }
}
