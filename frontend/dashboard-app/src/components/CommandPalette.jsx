import React, { useEffect, useState, useContext, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../services/AuthContext.jsx";
import "./commandPalette.css";

export default function CommandPalette({ isOpen, onClose }) {
  const navigate = useNavigate();
  const { hasRole } = useContext(AuthContext);

  const [query, setQuery] = useState("");
  const [highlight, setHighlight] = useState(0);

  const inputRef = useRef(null);
  const isAdmin = hasRole("admin");

  // ============================
  // ROLE‑AWARE ROUTE DEFINITIONS
  // ============================
  const routes = [
    { label: "Dashboard Home", path: "/admin", admin: false },
    { label: "PELM Panel", path: "/admin/pelm", admin: true },
    { label: "Anomaly Detection", path: "/admin/anomaly", admin: true },
    { label: "IDRIM Panel", path: "/admin/idrim", admin: true },
    { label: "Validators", path: "/admin/validators", admin: true },
    { label: "Repo Health", path: "/admin/repo-health", admin: true },
    { label: "Git Health", path: "/admin/git-health", admin: true }
  ].filter(r => (r.admin ? isAdmin : true));

  // ============================
  // FUZZY SEARCH
  // ============================
  const filtered = routes.filter(r =>
    r.label.toLowerCase().includes(query.toLowerCase())
  );

  // ============================
  // KEYBOARD HANDLING (LOCAL)
  // ============================
  useEffect(() => {
    if (!isOpen) return;

    const handler = (e) => {
      if (e.key === "Escape") {
        onClose();
        return;
      }

      if (e.key === "ArrowDown") {
        setHighlight((h) => Math.min(h + 1, filtered.length - 1));
        return;
      }

      if (e.key === "ArrowUp") {
        setHighlight((h) => Math.max(h - 1, 0));
        return;
      }

      if (e.key === "Enter") {
        const target = filtered[highlight];
        if (target) {
          navigate(target.path);
          onClose();
        }
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [isOpen, filtered, highlight, navigate, onClose]);

  // ============================
  // AUTO‑FOCUS INPUT WHEN OPEN
  // ============================
  useEffect(() => {
    if (isOpen && inputRef.current) {
      setTimeout(() => inputRef.current.focus(), 10);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  // ============================
  // RENDER
  // ============================
  return (
    <div className="cmd-overlay" onClick={onClose}>
      <div className="cmd-container" onClick={(e) => e.stopPropagation()}>

        <input
          ref={inputRef}
          className="cmd-input"
          placeholder="Search panels…"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setHighlight(0);
          }}
        />

        <div className="cmd-results">
          {filtered.length === 0 && (
            <div className="cmd-empty">No matches</div>
          )}

          {filtered.map((r, i) => (
            <div
              key={r.path}
              className={i === highlight ? "cmd-item active" : "cmd-item"}
              onMouseEnter={() => setHighlight(i)}
              onClick={() => {
                navigate(r.path);
                onClose();
              }}
            >
              {r.label}
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}
