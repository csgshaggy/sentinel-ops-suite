import { useEffect, useState } from "react";
import { governanceService } from "../services/governanceService";

export function useGovernanceHistory(repoId) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);

    governanceService
      .getHistory(repoId)
      .then((res) => setData(res))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [repoId]);

  return { data, loading, error };
}
