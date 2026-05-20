// /src/components/settings/ThemeSettings.jsx
// Hybrid settings component:
// - Local state for themeMode + accentColor
// - Commits changes to SettingsContext
// - No API calls, no save button (handled by SettingsFooter)

import { useEffect, useState } from "react";
import { useSettings } from "../../context/SettingsContext.jsx";

const ACCENT_COLORS = [
  "#00e5ff",
  "#ff4081",
  "#7c4dff",
  "#00e676",
  "#ffea00",
  "#ff9100",
  "#ff3d00",
];

export default function ThemeSettings() {
  const { settings, updateSetting } = useSettings();

  // Local hybrid state
  const [mode, setMode] = useState("light");
  const [accent, setAccent] = useState("#00e5ff");

  // Sync local state when settings load
  useEffect(() => {
    if (settings) {
      setMode(settings.themeMode || "light");
      setAccent(settings.accentColor || "#00e5ff");
    }
  }, [settings]);

  // Commit theme mode
  const commitMode = (value) => {
    setMode(value);
    updateSetting("themeMode", value);
  };

  // Commit accent color
  const commitAccent = (value) => {
    setAccent(value);
    updateSetting("accentColor", value);
  };

  return (
    <div className="glass-panel" style={{ padding: "24px" }}>
      <h2 style={{ marginBottom: "16px" }}>Theme Settings</h2>

      {/* Theme Mode */}
      <div style={{ marginBottom: "20px" }}>
        <label style={{ opacity: 0.8 }}>Theme Mode</label>
        <div style={{ marginTop: "10px", display: "flex", gap: "12px" }}>
          {["light", "dark", "system"].map((m) => (
            <button
              key={m}
              onClick={() => commitMode(m)}
              style={{
                padding: "10px 16px",
                borderRadius: "var(--radius)",
                background:
                  mode === m ? "var(--accent)" : "rgba(255,255,255,0.06)",
                color: mode === m ? "#000" : "var(--text-primary)",
                fontWeight: mode === m ? "700" : "500",
                border:
                  mode === m
                    ? "1px solid var(--accent-soft)"
                    : "1px solid transparent",
                cursor: "pointer",
              }}
            >
              {m.charAt(0).toUpperCase() + m.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Accent Color */}
      <div style={{ marginBottom: "20px" }}>
        <label style={{ opacity: 0.8 }}>Accent Color</label>
        <div
          style={{
            marginTop: "12px",
            display: "flex",
            gap: "12px",
            flexWrap: "wrap",
          }}
        >
          {ACCENT_COLORS.map((c) => (
            <div
              key={c}
              onClick={() => commitAccent(c)}
              style={{
                width: "36px",
                height: "36px",
                borderRadius: "50%",
                background: c,
                border:
                  accent === c
                    ? "3px solid var(--accent)"
                    : "2px solid rgba(255,255,255,0.2)",
                cursor: "pointer",
                boxShadow:
                  accent === c ? "0 0 10px rgba(255,255,255,0.4)" : "none",
              }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
