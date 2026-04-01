import React, { useEffect, useState } from "react";

type DiffLine = {
  type: "add" | "remove" | "context";
  text: string;
};

export const MakefileDiffViewer: React.FC = () => {
  const [diff, setDiff] = useState<DiffLine[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDiff = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch("/api/makefile/diff");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setDiff(data.lines || []);
      } catch (e: any) {
        setError(e.message || "Failed to load diff");
      } finally {
        setLoading(false);
      }
    };
    fetchDiff();
  }, []);

  if (loading) return <div>Loading Makefile diff…</div>;
  if (error) return <div style={{ color: "red" }}>Error: {error}</div>;

  return (
    <div style={{ fontFamily: "monospace", fontSize: 13 }}>
      {diff.map((line, idx) => {
        let color = "#ccc";
        if (line.type === "add") color = "#2ecc71";
        if (line.type === "remove") color = "#e74c3c";
        return (
          <div key={idx} style={{ whiteSpace: "pre", color }}>
            {line.text}
          </div>
        );
      })}
    </div>
  );
};
