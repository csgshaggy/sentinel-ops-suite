import React from "react";
import TextInput from "../../components/forms/TextInput";

export default function FormField({
  id,
  label,
  type = "text",
  value,
  onChange,
  autoComplete,
  required = false,
  error = "",
  valid = false,
  className = "",
}) {
  return (
    <div className={`ui-form-field ${className}`}>
      <TextInput
        id={id}
        label={label}
        type={type}
        value={value}
        onChange={onChange}
        autoComplete={autoComplete}
        required={required}
        error={error}
        valid={valid}
      />
    </div>
  );
}
