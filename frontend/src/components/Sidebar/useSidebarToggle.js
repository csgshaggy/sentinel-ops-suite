// useSidebarToggle.js — Segment 1

import { useState, useCallback } from "react";

export function useSidebarToggle(initial = false) {
  const [collapsed, setCollapsed] = useState(initial);
// useSidebarToggle.js — Segment 2

  const toggle = useCallback(() => {
    setCollapsed(prev => !prev);
  }, []);

  const set = useCallback((value) => {
    setCollapsed(Boolean(value));
  }, []);

  return { collapsed, toggle, set };
}
// sidebarThemeValidator.js — Segment 1

const REQUIRED_TOKENS = [
  "--sidebar-bg",
  "--sidebar-border",
  "--sidebar-width",
  "--sidebar-width-collapsed",
  "--text-primary",
  "--text-secondary",
  "--nav-hover-bg",
  "--nav-active-bg",
  "--button-ghost-bg",
  "--button-ghost-hover-bg",
  "--button-ghost-active-bg",
  "--radius-md",
  "--space-2",
  "--space-3",
  "--space-4",
  "--font-size-sm",
  "--font-weight-medium",
  "--ease-out"
];
// sidebarThemeValidator.js — Segment 2

export function validateSidebarTokens() {
  const root = document.documentElement;
  const styles = getComputedStyle(root);

  const missing = REQUIRED_TOKENS.filter(
    token => !styles.getPropertyValue(token)?.trim()
  );
// sidebarThemeValidator.js — Segment 3

  if (missing.length > 0) {
    console.groupCollapsed(
      "%c[Sidebar Token Validator] Missing CSS Variables",
      "color:#ff5555;font-weight:bold;"
    );

    missing.forEach(token => {
      console.log(
        `%cMissing: ${token}`,
        "color:#ff8888;font-weight:600;"
      );
    });

    console.groupEnd();
  }
}
// sidebarThemeValidator.js — Segment 3

  if (missing.length > 0) {
    console.groupCollapsed(
      "%c[Sidebar Token Validator] Missing CSS Variables",
      "color:#ff5555;font-weight:bold;"
    );

    missing.forEach(token => {
      console.log(
        `%cMissing: ${token}`,
        "color:#ff8888;font-weight:600;"
      );
    });

    console.groupEnd();
  }
}

