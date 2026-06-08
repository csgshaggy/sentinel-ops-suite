// /src/components/ToastManager.jsx

import { useState, useEffect } from "react";
import "../styles/theme.css";
import { toast } from "./toastBus.js";   // event bus

// Named export (kept exactly as-is)
export function ToastManager({ children }) {
  const [toasts, setToasts] = useState([]);

  useEffect(() => {
    const handler = (toastEvent) => {
      const id = Date.now() + Math.random();

      setToasts((prev) => [...prev, { id, ...toastEvent }]);

      // Auto-remove after duration
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
      }, toastEvent.duration || 4000);
    };

    toast.listeners.push(handler);

    return () => {
      toast.listeners = toast.listeners.filter((l) => l !== handler);
    };
  }, []);

  return (
    <>
      {children}

      <div
        style={{
          position: "fixed",
          top: "20px",
          right: "20px",
          zIndex: 99999,
          display: "flex",
          flexDirection: "column",
          gap: "12px",
        }}
      >
        {toasts.map((t) => (
          <Toast key={t.id} type={t.type} message={t.message} />
        ))}
      </div>
    </>
  );
}

// Re-export toast so other files can import { toast }
export { toast };

function Toast({ type, message }) {
  const colors = {
    success: "var(--color-success)",
    error: "var(--color-danger)",
    warning: "var(--color-warning)",
    info: "var(--accent)",
  };

  return (
    <div
      className="glass"
      style={{
        padding: "14px 18px",
        borderRadius: "var(--radius)",
        minWidth: "260px",
        maxWidth: "360px",
        color: "white",
        border: `1px solid ${colors[type] || "var(--accent)"}`,
        boxShadow: `0 0 12px ${colors[type] || "var(--accent)"}55`,
        backdropFilter: "blur(8px)",
        fontSize: "0.95rem",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        animation: "fadeIn 0.25s ease-out",
      }}
    >
      <span>{message}</span>

      <button
        onClick={(e) => {
          e.target.parentElement.style.opacity = 0;
          setTimeout(() => {
            e.target.parentElement.remove();
          }, 200);
        }}
        style={{
          marginLeft: "12px",
          background: "transparent",
          border: "none",
          color: "white",
          cursor: "pointer",
          fontSize: "1.1rem",
          opacity: 0.7,
        }}
      >
        ×
      </button>
    </div>
  );
}

// ✅ Default export added — fixes Vite + validator + Profile.jsx import
export default ToastManager;
