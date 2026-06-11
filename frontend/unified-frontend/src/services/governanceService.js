import {
  fetchGovernanceHistory,
  fetchGovernanceSnapshot,
  fetchGovernanceKpis,
} from "../api/governance";

export const governanceService = {
  // Fetch governance run history
  getHistory: (repoId) => fetchGovernanceHistory(repoId),

  // Fetch snapshot for a specific run
  getSnapshot: (runId) => fetchGovernanceSnapshot(runId),

  // Fetch governance KPIs (Step‑3)
  getKpis: () => fetchGovernanceKpis(),
};
