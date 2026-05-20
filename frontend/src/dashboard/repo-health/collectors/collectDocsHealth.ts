/**
 * collectDocsHealth.ts
 * --------------------
 * Collector for documentation health.
 * Returns a normalized structure for RepoHealth.
 */

export async function collectDocsHealth() {
  try {
    const res = await fetch("/api/docs/health");

    if (!res.ok) {
      return { ok: false, score: 0, detail: {} };
    }

    const data = await res.json();

    return {
      ok: true,
      score: data.score ?? 0,
      detail: data,
    };
  } catch {
    return {
      ok: false,
      score: 0,
      detail: {},
    };
  }
}
