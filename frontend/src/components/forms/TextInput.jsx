import React from "react";
import "./TextInput.css";

export default function TextInput({
  id,
  label,
  type = "text",
  value,
  onChange,
  autoComplete,
  required = false,
  error = "",
  valid = false,
}) {
  const fieldClassName = [
    "textinput-field",
    error ? "textinput-error-border" : "",
    !error && valid ? "textinput-valid-border" : "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div className="textinput-wrapper">
      {label && (
        <label htmlFor={id} className="textinput-label">
          {label}
        </label>
      )}

      <input
        id={id}
        name={id}
        type={type}
        value={value}
        onChange={onChange}
        autoComplete={autoComplete}
        required={required}
        className={fieldClassName}
      />

      {error && <div className="textinput-error">{error}</div>}
    </div>
  );
}
