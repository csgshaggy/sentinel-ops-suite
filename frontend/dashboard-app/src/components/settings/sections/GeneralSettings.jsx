// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/components/settings/GeneralSettings.jsx

import React, { useEffect, useState } from "react";

export default function GeneralSettings() {
  // Existing settings
  const [showProfile, setShowProfile] = useState(true);
  const [use24h, setUse24h] = useState(false);
  const [showSeconds, setShowSeconds] = useState(true);
  const [showDay, setShowDay] = useState(false);
  const [showClock, setShowClock] = useState(true);

  // New settings
  const [defaultPage, setDefaultPage] = useState("dashboard");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [toastEnabled, setToastEnabled] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(0);
  const [displayName, setDisplayName] = useState("");

  // Load saved preferences
  useEffect(() => {
    const load = (key, setter, transform = (v) => v) => {
      const saved = localStorage.getItem(key);
      if (saved !== null) setter(transform(saved));
    };

    load("settings.showProfile", setShowProfile, (v) => v === "true");
    load("settings.use24h", setUse24h, (v) => v === "true");
    load("settings.showSeconds", setShowSeconds, (v) => v === "true");
    load("settings.showDay", setShowDay, (v) => v === "true");
    load("settings.showClock", setShowClock, (v) => v === "true");

    load("settings.defaultPage", setDefaultPage);
    load("settings.sidebarCollapsed", setSidebarCollapsed, (v) => v === "true");
    load("settings.soundEnabled", setSoundEnabled, (v) => v === "true");
    load("settings.toastEnabled", setToastEnabled, (v) => v === "true");
    load("settings.autoRefresh", setAutoRefresh, (v) => Number(v));
    load("settings.displayName", setDisplayName);
  }, []);

  // Save helper
  const save = (key, value) => localStorage.setItem(key, value);

  return (
    <div className="settings-section">

      {/* ITEM 1 — Show Profile */}
      <div className="settings-item">
        <label className="settings-label">
          <input
            type="checkbox"
            checked={showProfile}
            onChange={() => {
              const v = !showProfile;
              setShowProfile(v);
              save("settings.showProfile", v);
            }}
          />
          Display username profile circle in TopBar
        </label>
      </div>

      {/* NEW — Show Clock */}
      <div className="settings-item">
        <label className="settings-label">
          <input
            type="checkbox"
            checked={showClock}
            onChange={() => {
              const v = !showClock;
              setShowClock(v);
              save("settings.showClock", v);
            }}
          />
          Show clock in TopBar
        </label>
      </div>

      {/* ITEM 2 — 24-Hour Clock */}
      <div className="settings-item">
        <label className="settings-label">
          <input
            type="checkbox"
            checked={use24h}
            onChange={() => {
              const v = !use24h;
              setUse24h(v);
              save("settings.use24h", v);
            }}
          />
          Use 24-hour clock format
        </label>
      </div>

      {/* ITEM 3 — Show Seconds */}
      <div className="settings-item">
        <label className="settings-label">
          <input
            type="checkbox"
            checked={showSeconds}
            onChange={() => {
              const v = !showSeconds;
              setShowSeconds(v);
              save("settings.showSeconds", v);
            }}
          />
          Show seconds on clock
        </label>
      </div>

      {/* ITEM 4 — Show Day of Week */}
      <div className="settings-item">
        <label className="settings-label">
          <input
            type="checkbox"
            checked={showDay}
            onChange={() => {
              const v = !showDay;
              setShowDay(v);
              save("settings.showDay", v);
            }}
          />
          Show day of week in TopBar
        </label>
      </div>

      {/* ITEM A — Default Landing Page */}
      <div className="settings-item">
        <label className="settings-label">
          Default landing page:
          <select
            value={defaultPage}
            onChange={(e) => {
              setDefaultPage(e.target.value);
              save("settings.defaultPage", e.target.value);
            }}
          >
            <option value="dashboard">Dashboard</option>
            <option value="alerts">Alerts</option>
            <option value="analytics">Analytics</option>
            <option value="systems">Systems & Modules</option>
          </select>
        </label>
      </div>

      {/* ITEM B — Sidebar Collapsed by Default */}
      <div className="settings-item">
        <label className="settings-label">
          <input
            type="checkbox"
            checked={sidebarCollapsed}
            onChange={() => {
              const v = !sidebarCollapsed;
              setSidebarCollapsed(v);
              save("settings.sidebarCollapsed", v);
            }}
          />
          Start with sidebar collapsed
        </label>
      </div>

      {/* ITEM C — Notification Sounds */}
      <div className="settings-item">
        <label className="settings-label">
          <input
            type="checkbox"
            checked={soundEnabled}
            onChange={() => {
              const v = !soundEnabled;
              setSoundEnabled(v);
              save("settings.soundEnabled", v);
            }}
          />
          Enable notification sounds
        </label>
      </div>

      {/* ITEM D — Toast Notifications */}
      <div className="settings-item">
        <label className="settings-label">
          <input
            type="checkbox"
            checked={toastEnabled}
            onChange={() => {
              const v = !toastEnabled;
              setToastEnabled(v);
              save("settings.toastEnabled", v);
            }}
          />
          Enable toast notifications
        </label>
      </div>

      {/* ITEM E — Auto-Refresh Interval */}
      <div className="settings-item">
        <label className="settings-label">
          Auto-refresh interval (seconds):
          <input
            type="number"
            min="0"
            value={autoRefresh}
            onChange={(e) => {
              const v = Number(e.target.value);
              setAutoRefresh(v);
              save("settings.autoRefresh", v);
            }}
          />
        </label>
      </div>

      {/* ITEM F — Display Name Override */}
      <div className="settings-item">
        <label className="settings-label">
          Display name override:
          <input
            type="text"
            value={displayName}
            onChange={(e) => {
              setDisplayName(e.target.value);
              save("settings.displayName", e.target.value);
            }}
          />
        </label>
      </div>

    </div>
  );
}
