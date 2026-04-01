import React, { useEffect, useState } from "react";

type MakefileHealth = {
  status: "ok" | "drift" | "missing";
  adds: number;
  removes: number;
  message: string;
};

export const MakefileDriftTile: React.FC = () => {
  const [data, setData] = useState<MakefileHealth | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHealth = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch("/api/makefile/health");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        setData(json);
      } catch (e: any) {
        setError(e.message || "Failed to load Makefile health");
      } finally {
        setLoading(false);
      }
    };
    fetchHealth();
  }, []);

  if (loading) return <div>Makefile: checking…</div>;
  if (error) return <div style={{ color: "red" }}>Makefile error: {error}</div>;
  if (!data) return <div>Makefile: no data</div>;

  const bg =
    data.status === "ok" ? "#ddffdd" : data.status === "drift" ? "#ffefdd" : "#ffdddd";
  const border =
    data.status === "ok" ? "#2ecc71" : data.status === "drift" ? "#f39c12" : "#e74c3c";

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
      <strong>Makefile Drift</strong>
      <div>{data.message}</div>
      <div style={{ fontSize: 12, marginTop: 4 }}>
        +{data.adds} / -{data.removes} vs snapshot
      </div>
    </div>
  );
};
