// ============================================
// TextInput.demo.jsx
// Path: frontend/src/ui-kit/components/TextInput/TextInput.demo.jsx
// Demo showcasing variant support
// ============================================

import React, { useState } from "react";
import TextInput from "./TextInput";
import "./TextInput.css";
import "./TextInput.theme.css";
import "./TextInput.variants.css";

export default function TextInputDemo() {
  const [value, setValue] = useState("");
  const [secureValue, setSecureValue] = useState("");
  const [warnValue, setWarnValue] = useState("");
  const [successValue, setSuccessValue] = useState("");
  const [errorValue, setErrorValue] = useState("");

  const dynamicError =
    errorValue.length > 0 && errorValue.length < 4
      ? "Minimum 4 characters required"
      : "";

  return (
    <div className="operator-panel" style={{ padding: 20, maxWidth: 480 }}>
      <h2 style={{ marginBottom: 16 }}>TextInput Variant Demo</h2>

      <TextInput
        label="Default"
        placeholder="Type something..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />

      <div style={{ height: 16 }} />

      <TextInput
        label="Success Variant"
        variant="success"
        placeholder="Looks good"
        value={successValue}
        onChange={(e) => setSuccessValue(e.target.value)}
      />

      <div style={{ height: 16 }} />

      <TextInput
        label="Warning Variant"
        variant="warning"
        placeholder="Check this"
        value={warnValue}
        onChange={(e) => setWarnValue(e.target.value)}
      />

      <div style={{ height: 16 }} />

      <TextInput
        label="Secure Variant"
        variant="secure"
        type="password"
        placeholder="Enter secret"
        value={secureValue}
        onChange={(e) => setSecureValue(e.target.value)}
      />

      <div style={{ height: 16 }} />

      <TextInput
        label="Error Variant"
        variant="error"
        placeholder="Something is wrong"
        value={errorValue}
        onChange={(e) => setErrorValue(e.target.value)}
        error={dynamicError}
      />
    </div>
  );
}
