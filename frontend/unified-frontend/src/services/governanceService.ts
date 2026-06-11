import { fetchGovernanceHistory } from "../api/governance";

export const governanceService = {
  getHistory: (repoId: number) => fetchGovernanceHistory(repoId),
};
