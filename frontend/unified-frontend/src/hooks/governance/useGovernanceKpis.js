import { useEffect, useState } from "react";

export function useGovernanceKpis() {
  const [kpis, setKpis] = useState({
    complianceCoverage: null,
    openActions: null,
    slaDrift: null,
    policyExceptions: null,
  });

  const [loading, setLoading] = useState(true);

  // Step‑2: Frontend-only simulated KPI logic
  useEffect(() => {
    const simulated = {
      complianceCoverage: 92,
      openActions: 14,
      slaDrift: 3.2,
      policyExceptions: 7,
    };

    setKpis(simulated);
    setLoading(false);
  }, []);

  return { kpis, loading };
}
