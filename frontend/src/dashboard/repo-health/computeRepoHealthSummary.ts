/**
 * computeRepoHealthSummary.ts
 * ---------------------------
 * Produces a single summary score + status for the entire repo.
 */

export function computeRepoHealthSummary(health: any) {
  if (!health) {
    return { score: 0, status: "unknown", breakdown: {} };
  }

  const subsystems = {
    mfa: health.mfa?.score ?? 0,
    docs: health.docs?.score ?? 0,
    structure: health.structure?.score ?? 0,
    deps: health.deps?.score ?? 0,
    makefile: health.makefile?.score ?? 0,
  };

  const values = Object.values(subsystems);
  const score = Math.round(values.reduce((a, b) => a + b, 0) / values.length);

  let status = "unknown";
  if (score >= 90) status = "excellent";
  else if (score >= 75) status = "good";
  else if (score >= 50) status = "warning";
  else status = "critical";

  return {
    score,
    status,
    breakdown: subsystems,
  };
}
