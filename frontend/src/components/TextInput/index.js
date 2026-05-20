/* ============================================
   /frontend/src/ui-kit/index.js
   Global UI Kit Export Surface
   ============================================ */

export { default as TextInput } from "./components/TextInput";

/* ============================================
   /frontend/src/ui-kit/components/TextInput/index.js
   Component Barrel
   ============================================ */

import TextInput from "./TextInput.jsx";
import "./TextInput.css";
import "./TextInput.theme.css";

export default TextInput;

/* ============================================
   /frontend/src/ui-kit/components/TextInput/TextInput.jsx
   Operator-Grade Component Wrapper
   ============================================ */

import React from "react";
import "./TextInput.css";
import "./TextInput.theme.css";

export default function TextInput({
  label,
  error,
  disabled,
  ...props
}) {
  return (
    <div className="textinput-wrapper">
      {label && <label className="textinput-label">{label}</label>}

      <input
        className={`textinput-field ${error ? "error" : ""}`}
        disabled={disabled}
        {...props}
      />

      {error && <div className="textinput-error-text">{error}</div>}
    </div>
  );
}

/* ============================================
   /frontend/src/ui-kit/theme.js
   Global Theme Controller
   ============================================ */

export function setTheme(theme) {
  if (!["light", "dark"].includes(theme)) return;
  document.documentElement.setAttribute("data-theme", theme);
}

export function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  setTheme(next);
}

/* ============================================
   /frontend/src/ui-kit/global.css
   Global UI Kit Stylesheet
   ============================================ */

/* Import component-level styles */
@import "./components/TextInput/TextInput.css";
@import "./components/TextInput/TextInput.theme.css";

/* Future components will be added here */

/* ============================================
   /frontend/src/ui-kit/index.js
   Updated Export Surface
   ============================================ */

export { default as TextInput } from "./components/TextInput";
export * as Theme from "./theme";


