// Fetch Governance Run History
export async function fetchGovernanceHistory(repoId) {
  const res = await fetch(`/api/governance/history?repo_id=${repoId}`);

  if (!res.ok) {
    throw new Error(`Failed to fetch governance history: ${res.status}`);
  }

  return res.json();
}

// Fetch Governance Snapshot for a specific run
export async function fetchGovernanceSnapshot(runId) {
  const res = await fetch(`/api/governance/snapshot/${runId}`);

  if (!res.ok) {
    throw new Error(`Failed to fetch snapshot: ${res.status}`);
  }

  return res.json();
}
