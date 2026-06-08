// /src/components/CommandPalette.jsx
import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./CommandPalette.css";

export default function CommandPalette({ isOpen, onClose }) {
  const navigate = useNavigate();
  const inputRef = useRef(null);

  const [query, setQuery] = useState("");
  const [highlight, setHighlight] = useState(0);

  const commands = [
    { label: "Dashboard", path: "/dashboard" },
    { label: "Admin Panel", path: "/admin" },
    { label: "PEL Manager", path: "/admin/pelm" },
    { label: "Anomaly Detection", path: "/admin/anomaly" },
    { label: "Identity & Roles", path: "/admin/idrim" },
    { label: "Validators", path: "/admin/validators" },
    { label: "Repo Health", path: "/admin/repo-health" },
    { label: "Git Health", path: "/admin/git-health" },
    { label: "User Preferences", path: "/preferences" },
    { label: "Logout", path: "/logout" },
  ];

  const filtered = commands.filter((cmd) =>
    cmd.label.toLowerCase().includes(query.toLowerCase())
  );

  /* Auto-focus input when opened */
  useEffect(() => {
    if (isOpen && inputRef.current) {
      setTimeout(() => inputRef.current.focus(), 10);
    }
  }, [isOpen]);

  /* Keyboard navigation */
  useEffect(() => {
    if (!isOpen) return;

    const handler = (e) => {
      if (e.key === "Escape") {
        onClose();
      }

      if (e.key === "ArrowDown") {
        e.preventDefault();
        setHighlight((h) => Math.min(h + 1, filtered.length - 1));
      }

      if (e.key === "ArrowUp") {
        e.preventDefault();
        setHighlight((h) => Math.max(h - 1, 0));
      }

      if (e.key === "Enter") {
        const cmd = filtered[highlight];
        if (cmd) {
          onClose();
          navigate(cmd.path);
        }
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [isOpen, filtered, highlight, navigate, onClose]);

  if (!isOpen) return null;

  return (
    <div className="palette-overlay" onClick={onClose}>
      <div
        className="palette-container"
        onClick={(e) => e.stopPropagation()}
      >
        <input
          ref={inputRef}
          className="palette-input"
          placeholder="Search commands…"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setHighlight(0);
          }}
        />

        <div className="palette-results">
          {filtered.length === 0 && (
            <div className="palette-empty">No results</div>
          )}

          {filtered.map((cmd, idx) => (
            <div
              key={cmd.label}
              className={`palette-item ${
                idx === highlight ? "active" : ""
              }`}
              onClick={() => {
                onClose();
                navigate(cmd.path);
              }}
            >
              {cmd.label}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
