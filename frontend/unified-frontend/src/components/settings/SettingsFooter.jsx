// /src/components/settings/SettingsFooter.jsx
// Unified Settings Footer — Reset / Apply / Save
// Clean, deterministic, backend‑aligned, deep‑clone baseline snapshots

import { useEffect, useState } from "react";
import { useSettings } from "../../context/SettingsContext.jsx";

export default function SettingsFooter() {
  const { settings, saveSettings } = useSettings();
  const [saving, setSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState(null);

  // Baseline snapshot of settings when last successfully applied/saved/reset
  const [baseline, setBaseline] = useState(null);

  // -----------------------------------------
  // BACKEND‑ALIGNED DEFAULTS
  // Must match SettingsContext DEFAULTS exactly
  // -----------------------------------------
  const DEFAULTS = {
    displayName: "",
    landingPage: "dashboard",
    sidebarCollapsed: false,
    use24h: false,
    showSeconds: false,
    showDate: true,
    enableSounds: false,
    enableToasts: true,
    autoRefresh: 30,
    emailAlerts: false,
    darkMode: false,
    accentColor: "#00e5ff",
    themeMode: "light",
    sessionTimeout: 15,
  };

  // -----------------------------------------
  // Initialize baseline once when settings load
  // Deep clone to avoid reference mutation
  // -----------------------------------------
  useEffect(() => {
    if (!baseline && settings) {
      setBaseline(JSON.parse(JSON.stringify(settings)));
    }
  }, [baseline, settings]);

  // -----------------------------------------
  // Detect pending changes
  // -----------------------------------------
  const hasChanges =
    !!baseline &&
    JSON.stringify(settings || {}) !== JSON.stringify(baseline || {});

  // -----------------------------------------
  // APPLY (save to backend)
  // -----------------------------------------
  const handleApply = async () => {
    if (!hasChanges || saving) return;

    try {
      setSaving(true);

      await saveSettings(settings);

      // Deep clone new baseline
      setBaseline(JSON.parse(JSON.stringify(settings)));
      setLastSaved(new Date());
    } catch (err) {
      console.error("Failed to apply settings:", err);
      if (window?.toast) window.toast.error("Failed to apply settings");
    } finally {
      setSaving(false);
    }
  };

  // -----------------------------------------
  // RESET (restore defaults)
  // -----------------------------------------
  const handleReset = async () => {
    if (saving) return;

    try {
      setSaving(true);

      await saveSettings(DEFAULTS);

      // Deep clone new baseline
      setBaseline(JSON.parse(JSON.stringify(DEFAULTS)));
      setLastSaved(new Date());
    } catch (err) {
      console.error("Failed to reset settings:", err);
      if (window?.toast) window.toast.error("Failed to reset settings");
    } finally {
      setSaving(false);
    }
  };

  // -----------------------------------------
  // SAVE (apply + toast)
  // -----------------------------------------
  const handleSave = async () => {
    if (!hasChanges || saving) return;

    try {
      await handleApply();
      if (window?.toast) window.toast.success("Settings saved");
    } catch (err) {
      console.error("Failed to save settings:", err);
      if (window?.toast) window.toast.error("Failed to save settings");
    }
  };

  // -----------------------------------------
  // Keyboard-first focus ring
  // -----------------------------------------
  const focusStyle = {
    outline: "2px solid var(--accent)",
    outlineOffset: "3px",
  };

  const applyFocusRing = (e) => {
    if (e.key === "Tab") {
      e.target.style.outline = focusStyle.outline;
      e.target.style.outlineOffset = focusStyle.outlineOffset;
    }
  };

  const clearFocusRing = (e) => {
    e.target.style.outline = "none";
  };

  // -----------------------------------------
  // RENDER
  // -----------------------------------------
  return (
    <div
      className="glass-panel"
      style={{
        position: "sticky",
        bottom: 0,
        zIndex: 50,
        backdropFilter: "blur(12px)",
        background: "rgba(0,0,0,0.45)",
        padding: "16px 24px",
        marginTop: "32px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        borderTop: "1px solid rgba(255,255,255,0.12)",
      }}
    >
      <div style={{ opacity: 0.7, fontSize: "0.85rem" }}>
        {lastSaved
          ? `Last saved: ${lastSaved.toLocaleTimeString()}`
          : hasChanges
          ? "Unsaved changes"
          : "All changes applied"}
      </div>

      <div style={{ display: "flex", gap: "12px" }}>
        <button
          className="btn-secondary"
          disabled={saving || !hasChanges}
          onClick={handleReset}
          onKeyDown={applyFocusRing}
          onBlur={clearFocusRing}
        >
          Reset
        </button>

        <button
          className="btn-secondary"
          disabled={saving || !hasChanges}
          onClick={handleApply}
          onKeyDown={applyFocusRing}
          onBlur={clearFocusRing}
        >
          Apply
        </button>

        <button
          className="btn-primary"
          disabled={saving || !hasChanges}
          onClick={handleSave}
          onKeyDown={applyFocusRing}
          onBlur={clearFocusRing}
        >
          {saving ? "Saving..." : "Save"}
        </button>
      </div>
    </div>
  );
}
