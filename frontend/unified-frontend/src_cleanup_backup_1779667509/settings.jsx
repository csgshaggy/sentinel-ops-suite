// /src/pages/settings.jsx
// Unified Settings Page — Clean container, sticky header + footer
// All logic lives in SettingsContext + component modules.

import { useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout.jsx";

import GeneralSettings from "../components/settings/GeneralSettings.jsx";
import ThemeSettings from "../components/settings/ThemeSettings.jsx";
import TimeSettings from "../components/settings/TimeSettings.jsx";
import SessionSettings from "../components/settings/SessionSettings.jsx";

import SettingsFooter from "../components/settings/SettingsFooter.jsx";

export default function Settings() {
  const [tab, setTab] = useState(0);

  const tabs = ["General", "Theme", "Time", "Session"];

  return (
    <DashboardLayout>
      <div
        style={{
          width: "100%",
          maxWidth: "900px",
          margin: "0 auto",
          padding: "0 32px 120px 32px", // ensures footer never overlaps content
          color: "var(--text-primary)",
        }}
      >
        {/* --------------------------------------------- */}
        {/* Sticky Header                                 */}
        {/* --------------------------------------------- */}
        <div
          style={{
            position: "sticky",
            top: 0,
            zIndex: 60,
            paddingTop: "32px",
            paddingBottom: "16px",
            background: "rgba(0,0,0,0.65)",
            backdropFilter: "blur(12px)",
            borderBottom: "1px solid rgba(255,255,255,0.12)",
          }}
        >
          <h1
            className="text-glow"
            style={{
              marginBottom: "20px",
            }}
          >
            Settings
          </h1>

          {/* Tabs */}
          <div
            style={{
              display: "flex",
              gap: "12px",
              paddingBottom: "12px",
            }}
          >
            {tabs.map((label, index) => {
              const active = tab === index;
              return (
                <button
                  key={label}
                  onClick={() => setTab(index)}
                  className="btn-tab"
                  style={{
                    padding: "10px 18px",
                    borderRadius: "var(--radius)",
                    background: active
                      ? "var(--accent)"
                      : "rgba(255,255,255,0.06)",
                    color: active ? "#000" : "var(--text-primary)",
                    fontWeight: active ? "700" : "500",
                    border: active
                      ? "1px solid var(--accent-soft)"
                      : "1px solid transparent",
                    cursor: "pointer",
                  }}
                >
                  {label}
                </button>
              );
            })}
          </div>
        </div>

        {/* --------------------------------------------- */}
        {/* Tab Content                                   */}
        {/* --------------------------------------------- */}
        <div style={{ marginTop: "24px" }}>
          {tab === 0 && <GeneralSettings />}
          {tab === 1 && <ThemeSettings />}
          {tab === 2 && <TimeSettings />}
          {tab === 3 && <SessionSettings />}
        </div>

        {/* --------------------------------------------- */}
        {/* Sticky Footer                                 */}
        {/* --------------------------------------------- */}
        <SettingsFooter />
      </div>
    </DashboardLayout>
  );
}
