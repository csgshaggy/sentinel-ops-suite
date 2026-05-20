// dashboard/src/components/LogsViewer.tsx

import React, { useEffect, useRef, useState } from "react";

export default function LogsViewer({ logs }: { logs: string[] }) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [previousLogs, setPreviousLogs] = useState<string[]>([]);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    // Auto-scroll to bottom
    el.scrollTop = el.scrollHeight;

    // Track previous logs for highlighting
    setPreviousLogs(logs);
  }, [logs]);

  const isNewLine = (line: string, index: number) => {
    return previousLogs[index] !== line;
  };

  return (
    <div
      ref={containerRef}
      style={{
        marginTop: "1rem",
        padding: "1rem",
        background: "var(--bg-panel)",
        border: "1px solid var(--border)",
        borderRadius: "6px",
        height: "260px",
        overflowY: "auto",
        fontFamily: "monospace",
        fontSize: "0.85rem",
        whiteSpace: "pre-wrap",
      }}
    >
      {logs.length === 0 ? (
        <div style={{ color: "#888" }}>No logs available.</div>
      ) : (
        logs.map((line, i) => (
          <div
            key={i}
            style={{
              animation: isNewLine(line, i) ? "fadeIn 0.4s ease" : "none",
              color: isNewLine(line, i) ? "#4caf50" : "var(--text)",
            }}
          >
            {line}
          </div>
        ))
      )}

      {/* Fade-in animation */}
      <style>
        {`
          @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
          }
        `}
      </style>
    </div>
  );
}
