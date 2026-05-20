// File: src/components/dashboard/MfaStatusTile.tsx

import { useEffect, useState } from "react";
import api from "../../api/client";

export default function MfaStatusTile() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/dashboard/summary")
      .then((res) => {
        const tile = res.data.tiles?.find((t) => t.id === "mfa-status");
        setStatus(tile || null);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="tile">Loading MFA status…</div>;
  if (!status) return <div className="tile">MFA status unavailable</div>;

  return (
    <div className="tile">
      <h3>MFA Status</h3>
      <p>{status.value}</p>
    </div>
  );
}
