// frontend/dashboard-app/src/components/CommandPalette.tsx

import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./commandPalette.css";

interface Command {
  name: string;
  path: string;
}

export default function CommandPalette() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");

  const commands: Command[] = [
    { name: "Dashboard Home", path: "/admin" },
    { name: "PELM Panel", path: "/admin/pelm" },
    { name: "Anomaly Detection", path: "/admin/anomaly" },
    { name: "IDRIM Panel", path: "/admin/idrim" },
    { name: "Validators", path: "/admin/validators" },
    { name: "Repo Health", path: "/admin/repo-health" },
    { name: "Git Health", path: "/admin/git-health" },
  ];

  const filtered = commands.filter((cmd) =>
    cmd.name.toLowerCase().includes(query.toLowerCase())
  );

  // Open palette with Ctrl+K or Cmd+K
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      const isMac = navigator.platform.toUpperCase().includes("MAC");
      const hotkey = isMac ? e.metaKey && e.key === "k" : e.ctrlKey && e.key === "k";

      if (hotkey) {
        e.preventDefault();
        setOpen((prev) => !prev);
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  const handleSelect = (path: string) => {
    setOpen(false);
    setQuery("");
    navigate(path);
  };

  if (!open) return null;

  return (
    <div className="command-palette-overlay" onClick={() => setOpen(false)}>
      <div className="command-palette" onClick={(e) => e.stopPropagation()}>
        <input
          autoFocus
          className="command-input"
          placeholder="Type a command..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <div className="command-list">
          {filtered.length === 0 && (
            <div className="command-empty">No matching commands</div>
          )}

          {filtered.map((cmd) => (
            <div
              key={cmd.path}
              className="command-item"
              onClick={() => handleSelect(cmd.path)}
            >
              {cmd.name}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
