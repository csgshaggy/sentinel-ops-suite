// /src/context/SettingsContext.jsx
// Unified Settings Context
// - Loads settings from backend
// - Provides updateSetting() for granular edits
// - Provides saveSettings() for full persistence
// - Backend-aligned defaults
// - No UI logic, no toast logic, pure state + API

import { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";

const SettingsContext = createContext(null);

export function SettingsProvider({ children }) {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);

  // ---------------------------------------------
  // Backend-aligned defaults
  // ---------------------------------------------
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

  // ---------------------------------------------
  // Load settings from backend
  // ---------------------------------------------
  useEffect(() => {
    async function load() {
      try {
        const res = await axios.get("/api/settings", {
          withCredentials: true,
        });

        const data = res.data || {};

        // Merge backend values with defaults
        setSettings({ ...DEFAULTS, ...data });
        setAuthenticated(true);
      } catch (err) {
        console.error("Failed to load settings:", err);

        // Fallback to defaults
        setSettings(DEFAULTS);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  // ---------------------------------------------
  // Local update (does NOT save to backend)
  // ---------------------------------------------
  function updateSetting(key, value) {
    setSettings((prev) => ({
      ...prev,
      [key]: value,
    }));
  }

  // ---------------------------------------------
  // Save to backend (PATCH)
  // ---------------------------------------------
  async function saveSettings(newSettings) {
    try {
      const res = await axios.patch("/api/settings", newSettings, {
        withCredentials: true,
      });

      const saved = res.data || newSettings;

      // Replace local state with backend-confirmed values
      setSettings(saved);

      return saved;
    } catch (err) {
      console.error("Failed to save settings:", err);
      throw err;
    }
  }

  return (
    <SettingsContext.Provider
      value={{
        settings,
        loading,
        authenticated,
        updateSetting,
        saveSettings,
        DEFAULTS,
      }}
    >
      {children}
    </SettingsContext.Provider>
  );
}

export function useSettings() {
  return useContext(SettingsContext);
}
