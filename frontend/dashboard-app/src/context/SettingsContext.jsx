// dashboard-app/src/context/SettingsContext.jsx

import { createContext, useContext, useEffect, useState } from "react";
import { fetchSettings, updateSettings } from "../api/settingsApi";

const SettingsContext = createContext(null);

export const SettingsProvider = ({ children }) => {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load settings on mount
  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchSettings();
        setSettings(data);
      } catch (err) {
        console.error("Failed to load settings:", err);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  // Update settings (partial updates)
  const saveSettings = async (updates) => {
    try {
      const updated = await updateSettings(updates);

      // Merge partial updates into existing state
      setSettings((prev) => ({
        ...prev,
        ...updated,
      }));

      return updated;
    } catch (err) {
      console.error("Failed to update settings:", err);
      throw err;
    }
  };

  return (
    <SettingsContext.Provider
      value={{
        settings,
        loading,
        saveSettings,
      }}
    >
      {children}
    </SettingsContext.Provider>
  );
};

export const useSettings = () => useContext(SettingsContext);
