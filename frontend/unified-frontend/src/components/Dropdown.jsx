// /src/components/Dropdown.jsx

import { useState, useRef, useEffect } from "react";
import "../styles/theme.css";
import "../styles/buttons.css";
import "../components/Layout.css";

export default function Dropdown({
  label,
  items = [],
  align = "right", // "left" or "right"
  width = 180,
}) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  // Close when clicking outside
  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  return (
    <div ref={ref} style={{ position: "relative" }}>
      {/* Trigger */}
      <span
        onClick={() => setOpen((prev) => !prev)}
        style={{
          fontSize: "1.05rem",
          fontWeight: "600",
          color: "var(--text-primary)",
          cursor: "pointer",
          userSelect: "none",
        }}
      >
        {label}
      </span>

      {/* Menu */}
      {open && (
        <div
          className="glass"
          style={{
            position: "absolute",
            top: "42px",
            [align]: "0px",
            minWidth: `${width}px`,
            borderRadius: "var(--radius)",
            padding: "10px",
            display: "flex",
            flexDirection: "column",
            gap: "8px",
            boxShadow: "0 0 12px rgba(0,255,180,0.25)",
            zIndex: 9999,
          }}
        >
          {items.map((item, idx) => (
            <button
              key={idx}
              className={`btn-small ${item.danger ? "btn-danger" : ""}`}
              onClick={() => {
                setOpen(false);
                item.onClick?.();
              }}
              style={{
                width: "100%",
                textAlign: "left",
                ...(item.danger && {
                  background: "var(--color-danger)",
                  color: "#fff",
                }),
              }}
            >
              {item.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
