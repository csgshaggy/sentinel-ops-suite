import { useEffect, useState } from "react";
import { governanceService } from "../services/governanceService";

export function useGovernanceSnapshot(runId) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!runId) return;

    setLoading(true);

    governanceService
      .getSnapshot(runId)
      .then((res) => setData(res))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [runId]);

  return { data, loading, error };
}
