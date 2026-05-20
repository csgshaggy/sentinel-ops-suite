// src/components/layout/ThemeManager.jsx

import { useEffect } from "react";
import { useSettings } from "../../services/SettingsContext.jsx";

export default function ThemeManager() {
  const { settings } = useSettings();

  useEffect(() => {
    if (!settings) return;

    const theme = settings.theme || "system";
    const root = document.documentElement;

    const applyTheme = () => {
      if (theme === "light") {
        root.classList.remove("dark");
        root.classList.add("light");
      } else if (theme === "dark") {
        root.classList.remove("light");
        root.classList.add("dark");
      } else {
        // system theme
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        root.classList.toggle("dark", prefersDark);
        root.classList.toggle("light", !prefersDark);
      }
    };

    applyTheme();

    // Listen for system theme changes
    if (theme === "system") {
      const media = window.matchMedia("(prefers-color-scheme: dark)");
      const handler = () => applyTheme();
      media.addEventListener("change", handler);
      return () => media.removeEventListener("change", handler);
    }
  }, [settings]);

  return null;
}
