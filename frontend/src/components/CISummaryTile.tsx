import React, { useEffect, useState } from "react";

type CISummary = {
  backend: "ok" | "fail";
  frontend: "ok" | "fail";
  doctor: "ok" | "fail";
  makefile: "clean" | "drift" | "missing";
  timestamp: string;
};

export const CISummaryTile: React.FC = () => {
  const [data, setData] = useState<CISummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const res = await fetch("/api/ci/summary");
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

  if (loading) return <div>CI Summary: checking…</div>;
  if (error) return <div style={{ color: "red" }}>CI Summary error: {error}</div>;
  if (!data) return <div>No CI summary data</div>;

  const bg =
    data.backend === "ok" &&
    data.frontend === "ok" &&
    data.doctor === "ok" &&
    data.makefile === "clean"
      ? "#ddffdd"
      : "#ffefdd";

  const border =
    bg === "#ddffdd"
      ? "#2ecc71"
      : "#e67e22";

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
      <strong>CI Summary</strong>
      <div>Backend: {data.backend}</div>
      <div>Frontend: {data.frontend}</div>
      <div>Doctor: {data.doctor}</div>
      <div>Makefile: {data.makefile}</div>
      <div style={{ fontSize: 12, marginTop: 4 }}>Updated: {data.timestamp}</div>
    </div>
  );
};
