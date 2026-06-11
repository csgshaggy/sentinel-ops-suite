import {
  fetchGovernanceHistory,
  fetchGovernanceSnapshot,
} from "../api/governance";

export const governanceService = {
  // Fetch governance run history
  getHistory: (repoId) => fetchGovernanceHistory(repoId),

  // Fetch snapshot for a specific run
  getSnapshot: (runId) => fetchGovernanceSnapshot(runId),
};
