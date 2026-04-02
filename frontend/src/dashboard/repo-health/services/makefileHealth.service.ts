/**
 * makefileHealth.service.ts
 * -------------------------
 * Fetches Makefile health status from the backend.
 *
 * Backend endpoint:
 *   GET /api/repo/makefile/health
 */

export async function fetchMakefileHealth() {
  const res = await fetch("/api/repo/makefile/health");

  if (!res.ok) {
    throw new Error("Makefile health endpoint failed");
  }

  return res.json();
}
