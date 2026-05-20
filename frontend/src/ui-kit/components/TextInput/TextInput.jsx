// File: /home/ubuntu/sentinel-ops-suite/frontend/src/ui-kit/components/TextInput/TextInput.jsx
// Operator-Grade TextInput Component

import React, { forwardRef } from "react";
import variants from "./TextInput.variants.js";
import "./TextInput.css";
import "./TextInput.theme.css";
import "./TextInput.variants.css";

const TextInput = forwardRef(
  (
    {
      label,
      value,
      onChange,
      placeholder = "",
      error = "",
      variant = "default",
      disabled = false,
      className = "",
      ...rest
    },
    ref
  ) => {
    const variantClass = variants[variant] || variants.default;

    return (
      <div className={`ui-textinput-wrapper ${className}`}>
        {label && <label className="ui-textinput-label">{label}</label>}

        <input
          ref={ref}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          disabled={disabled}
          className={`ui-textinput ${variantClass} ${
            error ? "ui-textinput-error" : ""
          }`}
          {...rest}
        />

        {error && <div className="ui-textinput-error-message">{error}</div>}
      </div>
    );
  }
);

TextInput.displayName = "TextInput";

export default TextInput;
