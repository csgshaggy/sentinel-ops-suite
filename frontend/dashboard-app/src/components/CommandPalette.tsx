// frontend/dashboard-app/src/components/CommandPalette.tsx

import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./CommandPalette.css";

interface Command {
  name: string;
  path: string;
}

export default function CommandPalette() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");

  const commands: Command[] = [
    { name: "Home", path: "/admin" },
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

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.shiftKey && e.key === "P") {
        e.preventDefault();
        setOpen((prev) => !prev);
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  const handleSelect = (cmd: Command) => {
    navigate(cmd.path);
    setOpen(false);
    setQuery("");
  };

  if (!open) return null;

  return (
    <div className="command-palette">
      <div className="palette-box">
        <input
          autoFocus
          type="text"
          placeholder="Type a command..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <ul>
          {filtered.map((cmd) => (
            <li key={cmd.path} onClick={() => handleSelect(cmd)}>
              {cmd.name}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
