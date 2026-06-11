import { useEffect, useState } from "react";
import { governanceService } from "../services/governanceService";
import { GovernanceRunHistoryResponse } from "../api/governance";

export function useGovernanceHistory(repoId: number) {
  const [data, setData] = useState<GovernanceRunHistoryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    governanceService
      .getHistory(repoId)
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [repoId]);

  return { data, loading, error };
}
