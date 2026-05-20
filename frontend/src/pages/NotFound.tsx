// ============================================================================
// NotFound.tsx
// SentinelOps — 404 Fallback Page
// Glassy Neon UI • Operator‑Grade Clarity
// ============================================================================

import React from "react";
import { useNavigate } from "react-router-dom";
import "./NotFound.css"; // optional — safe even if missing

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "var(--bg-primary, #0a0f1a)",
        color: "var(--text-primary, #e0e6f0)",
        padding: "2rem",
      }}
    >
      <div
        style={{
          padding: "3rem 4rem",
          borderRadius: "16px",
          background: "rgba(255, 255, 255, 0.04)",
          backdropFilter: "blur(12px)",
          border: "1px solid rgba(0, 255, 255, 0.25)",
          boxShadow: "0 0 24px rgba(0, 255, 255, 0.15)",
          textAlign: "center",
          maxWidth: "480px",
        }}
      >
        <h1
          style={{
            fontSize: "3rem",
            marginBottom: "1rem",
            color: "var(--accent-neon, #00eaff)",
            textShadow: "0 0 12px rgba(0, 255, 255, 0.6)",
          }}
        >
          404
        </h1>

        <p style={{ marginBottom: "2rem", fontSize: "1.2rem" }}>
          The page you’re looking for doesn’t exist or has been moved.
        </p>

        <button
          onClick={() => navigate("/dashboard")}
          style={{
            padding: "0.75rem 1.5rem",
            borderRadius: "8px",
            border: "none",
            cursor: "pointer",
            fontSize: "1rem",
            background:
              "linear-gradient(90deg, #00eaff 0%, #00bcd4 100%)",
            color: "#000",
            fontWeight: 600,
            boxShadow: "0 0 12px rgba(0, 255, 255, 0.4)",
          }}
        >
          Return to Dashboard
        </button>
      </div>
    </div>
  );
}
