// File: /home/ubuntu/sentinel-ops-suite/frontend/src/ui-kit/components/TextInput/TextInput.demo.jsx
// Standalone Demo for TextInput Component

import React, { useState } from "react";
import TextInput from "./TextInput.jsx";
import variants from "./TextInput.variants.js";

export default function TextInputDemo() {
  const [value, setValue] = useState("");
  const [error, setError] = useState("");

  return (
    <div
      style={{
        padding: "20px",
        maxWidth: "400px",
        margin: "0 auto",
        display: "flex",
        flexDirection: "column",
        gap: "20px",
      }}
    >
      <h2 style={{ color: "white" }}>TextInput Demo</h2>

      {/* Default */}
      <TextInput
        label="Default"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Type something..."
        variant="default"
      />

      {/* Ghost */}
      <TextInput
        label="Ghost"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Ghost variant"
        variant="ghost"
      />

      {/* Solid */}
      <TextInput
        label="Solid"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Solid variant"
        variant="solid"
      />

      {/* Underline */}
      <TextInput
        label="Underline"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Underline variant"
        variant="underline"
      />

      {/* Compact */}
      <TextInput
        label="Compact"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Compact variant"
        variant="compact"
      />

      {/* Error Example */}
      <TextInput
        label="With Error"
        value={value}
        onChange={(e) => {
          const v = e.target.value;
          setValue(v);
          setError(v.length < 3 ? "Minimum 3 characters required" : "");
        }}
        placeholder="Triggers error under 3 chars"
        error={error}
      />
    </div>
  );
}
