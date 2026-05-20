// src/services/SettingsContext.jsx

import React, { createContext, useState, useEffect, useContext } from "react";

export const SettingsContext = createContext(null);

export function SettingsProvider({ children }) {
  const [isOpen, setIsOpen] = useState(false);
  const [timezone, setTimezone] = useState("UTC");
  const [sessionInfo, setSessionInfo] = useState(null);

  // Load saved timezone on mount
  useEffect(() => {
    const saved = localStorage.getItem("sentinel-timezone");
    if (saved) {
      setTimezone(saved);
    }
  }, []);

  // Persist timezone changes
  useEffect(() => {
    localStorage.setItem("sentinel-timezone", timezone);
  }, [timezone]);

  // Fetch session info
  useEffect(() => {
    const fetchSessionInfo = async () => {
      try {
        const res = await fetch("/api/auth/session-info", {
          method: "GET",
          credentials: "include",
        });

        if (!res.ok) throw new Error("bad response");

        const data = await res.json();
        setSessionInfo(data);
      } catch (err) {
        setSessionInfo({
          user: "Unknown",
          expires: "Unknown",
        });
      }
    };

    fetchSessionInfo();
  }, []);

  const openSettings = () => setIsOpen(true);
  const closeSettings = () => setIsOpen(false);

  return (
    <SettingsContext.Provider
      value={{
        isOpen,
        openSettings,
        closeSettings,
        timezone,
        setTimezone,
        sessionInfo,
      }}
    >
      {children}
    </SettingsContext.Provider>
  );
}

// ⭐ Custom Hook (the missing piece)
export function useSettings() {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error("useSettings must be used within a SettingsProvider");
  }
  return context;
}
