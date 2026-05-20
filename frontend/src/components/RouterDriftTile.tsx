import React, { useEffect, useState } from "react";

type RouterDrift = {
  status: "ok" | "degraded";
  missing: string[];
  extra: string[];
  ordered: boolean;
  expected_order: string[];
  actual_order: string[];
};

export const RouterDriftTile: React.FC = () => {
  const [data, setData] = useState<RouterDrift | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const res = await fetch("/api/plugins/router-drift");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        setData(json);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) return <div>Router Drift: checking…</div>;
  if (error) return <div style={{ color: "red" }}>Router Drift error: {error}</div>;
  if (!data) return <div>No router drift data</div>;

  const drift = data.status !== "ok";
  const bg = drift ? "#ffefdd" : "#ddffdd";
  const border = drift ? "#e67e22" : "#2ecc71";

  return (
    <div
      style={{
        padding: "0.75rem 1rem",
        borderRadius: 8,
        border: `1px solid ${border}`,
        background: bg,
        fontSize: 14,
      }}
    >
      <strong>Router Drift</strong>
      <div>{drift ? "Drift detected" : "Router tree clean"}</div>
      <div style={{ fontSize: 12, marginTop: 4 }}>
        Missing: {data.missing.length} | Extra: {data.extra.length}
      </div>
    </div>
  );
};
