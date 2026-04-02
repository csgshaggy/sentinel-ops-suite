/**
 * makefileHealth.service.ts
 * -------------------------
 * Fetches Makefile health status from the backend.
 * Updated to match all RepoHealth architecture changes as of April 2, 2026:
 * - Normalized return structure
 * - Deterministic error handling
 * - ESM-safe usage
 */

export async function fetchMakefileHealth() {
  try {
    const res = await fetch("/api/repo/makefile/health");

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
