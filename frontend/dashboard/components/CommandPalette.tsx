import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const COMMANDS = [
  { name: "Dashboard", path: "/" },
  { name: "PELM", path: "/pelm" },
  { name: "Anomaly Engine", path: "/anomaly" },
  { name: "IDRIM", path: "/idrim" },
  { name: "Validators", path: "/validators" },
  { name: "Repo Health", path: "/repo-health" },
  { name: "Git Integrity", path: "/git-health" },
];

export default function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((o) => !o);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  const filtered = COMMANDS.filter((cmd) =>
    cmd.name.toLowerCase().includes(query.toLowerCase())
  );

  if (!open) return null;

  return (
    <div className="absolute inset-0 bg-black bg-opacity-50 flex justify-center pt-20 z-50">
      <div className="bg-gray-900 w-96 rounded shadow-lg p-4 space-y-3">
        <input
          autoFocus
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type a command…"
          className="w-full px-3 py-2 rounded bg-gray-800 text-white"
        />

        <div className="max-h-64 overflow-auto space-y-1">
          {filtered.map((cmd) => (
            <div
              key={cmd.path}
              onClick={() => {
                navigate(cmd.path);
                setOpen(false);
              }}
              className="px-3 py-2 rounded hover:bg-gray-700 cursor-pointer"
            >
              {cmd.name}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
