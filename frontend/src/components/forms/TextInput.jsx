import React from "react";
import "./TextInput.css"; // optional if you want component‑level styling

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
  return (
    <div className="input-group">
      {label && (
        <label htmlFor={id} className="input-label">
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
        className={`input-field 
          ${error ? "input-error" : ""} 
          ${valid ? "input-valid" : ""}`}
      />

      {error && <div className="input-error-message">{error}</div>}
    </div>
  );
}
