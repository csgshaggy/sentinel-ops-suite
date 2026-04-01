import React, { useEffect, useState } from "react";

type RepoHealth = {
  makefile: "ok" | "drift" | "missing";
  router: "ok" | "drift";
  git: "ok" | "drift";
  system: "ok" | "warn" | "fail";
  score: number;
};

export const RepoHealthTile: React.FC = () => {
  const [data, setData] = useState<RepoHealth | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const res = await fetch("/api/repo/health");
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

  if (loading) return <div>Repo Health: checking…</div>;
  if (error) return <div style={{ color: "red" }}>Repo Health error: {error}</div>;
  if (!data) return <div>No repo health data</div>;

  const bg = data.score >= 90 ? "#ddffdd" : data.score >= 70 ? "#fff7cc" : "#ffdddd";
  const border = data.score >= 90 ? "#2ecc71" : data.score >= 70 ? "#f1c40f" : "#e74c3c";

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
      <strong>Repo Health</strong>
      <div>Score: {data.score}</div>
      <div style={{ fontSize: 12, marginTop: 4 }}>
        Makefile: {data.makefile} | Router: {data.router} | Git: {data.git} | System:{" "}
        {data.system}
      </div>
    </div>
  );
};
