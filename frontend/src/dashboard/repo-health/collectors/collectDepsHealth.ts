/**
 * collectDepsHealth.ts
 * --------------------
 * Collector for dependency health.
 * Matches all RepoHealth architecture updates as of April 2, 2026:
 * - ESM-safe explicit .ts imports
 * - Normalized collector return structure
 * - Deterministic scoring
 * - Snapshot-safe JSON output
 */

export async function collectDepsHealth() {
  try {
    const res = await fetch("/api/deps/health");

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
