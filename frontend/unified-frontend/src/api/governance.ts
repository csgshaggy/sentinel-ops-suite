export interface GovernanceRunHistoryItem {
  run_id: number;
  status: string;
  score: number;
  violations_count: number;
  triggered_at: string;
  completed_at: string | null;
}

export interface GovernanceRunHistoryResponse {
  repo_id: number;
  runs: GovernanceRunHistoryItem[];
}

export async function fetchGovernanceHistory(repoId: number): Promise<GovernanceRunHistoryResponse> {
  const res = await fetch(`/api/governance/history?repo_id=${repoId}`);

  if (!res.ok) {
    throw new Error(`Failed to fetch governance history: ${res.status}`);
  }

  return res.json();
}
