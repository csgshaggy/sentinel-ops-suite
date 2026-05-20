// src/components/layout/RefreshManager.jsx

import { useEffect } from "react";
import { useSettings } from "../../services/SettingsContext.jsx";

export default function RefreshManager() {
  const { settings } = useSettings();

  useEffect(() => {
    if (!settings) return;

    const interval = settings.auto_refresh_interval;

    // If disabled or invalid, do nothing
    if (!interval || interval <= 0) return;

    const emitRefresh = () => {
      window.dispatchEvent(new CustomEvent("global-refresh"));
    };

    // Emit immediately on mount
    emitRefresh();

    // Emit on interval
    const timer = setInterval(emitRefresh, interval * 1000);

    return () => clearInterval(timer);
  }, [settings]);

  return null;
}
