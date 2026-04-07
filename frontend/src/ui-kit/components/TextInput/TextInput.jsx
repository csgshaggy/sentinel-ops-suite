// ============================================
// TextInput.jsx
// Path: frontend/src/ui-kit/components/TextInput/TextInput.jsx
// Operator‑Grade TextInput Component w/ Variant Support
// ============================================

import React from "react";
import "./TextInput.css";
import "./TextInput.theme.css";
import "./TextInput.variants.css";
import { getTextInputVariantClass } from "./TextInput.variants";

export default function TextInput({
  label,
  error,
  disabled,
  variant = "default",
  className = "",
  ...props
}) {
  const variantClass = getTextInputVariantClass(variant);

  return (
    <div
      className={[
        "textinput-wrapper",
        disabled ? "disabled" : "",
        variantClass
      ]
        .filter(Boolean)
        .join(" ")}
    >
      {label && (
        <label className="textinput-label">
          {label}
        </label>
      )}

      <div className={`textinput-field ${error ? "has-error" : ""}`}>
        <input
          className={`textinput-input ${className}`}
          disabled={disabled}
          {...props}
        />
      </div>

      {error && (
        <div className="textinput-error">
          {error}
        </div>
      )}
    </div>
  );
}
