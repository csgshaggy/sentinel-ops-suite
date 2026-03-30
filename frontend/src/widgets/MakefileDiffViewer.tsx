import React, { useEffect, useState } from "react";
import { fetchMakefileDiff } from "../api/client";

export default function MakefileDiffViewer() {
  const [diff, setDiff] = useState<string[]>([]);
  const [health, setHealth] = useState<number>(100);
  const [warning, setWarning] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      const data = await fetchMakefileDiff();
      setDiff(data.diff);
      setHealth(data.health);
      setWarning(data.warning || null);
    };
    load();
  }, []);

  return (
    <div style={{ marginTop: "1rem" }}>
      <h3>Makefile Diff (Health: {health})</h3>

      {warning && (
        <div style={{ color: "#ff9800", marginBottom: "0.5rem" }}>
          {warning}
        </div>
      )}

      <pre
        style={{
          background: "#1e1e1e",
          color: "#dcdcdc",
          padding: "1rem",
          borderRadius: "6px",
          overflowX: "auto",
          whiteSpace: "pre-wrap",
          maxHeight: "300px",
        }}
      >
        {diff.map((line, i) => {
          let color = "#dcdcdc";
          if (line.startsWith("+")) color = "#4caf50";
          if (line.startsWith("-")) color = "#f44336";
          if (line.startsWith("@@")) color = "#ff9800";

          return (
            <div key={i} style={{ color }}>
              {line}
            </div>
          );
        })}
      </pre>
    </div>
  );
}
