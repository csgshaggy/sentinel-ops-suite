// File: src/pages/UiKitTest.jsx
// Operator-Grade UI-Kit Test Harness

import React, { useState } from "react";
import { TextInput, theme } from "@/ui-kit";

export default function UiKitTest() {
  const [value, setValue] = useState("");
  const [error, setError] = useState("");

  return (
    <div
      style={{
        padding: "32px",
        maxWidth: "600px",
        margin: "0 auto",
        display: "flex",
        flexDirection: "column",
        gap: "32px",
        color: "var(--ui-text)",
      }}
    >
      <h1 style={{ marginBottom: "8px" }}>UI‑Kit Test Page</h1>

      {/* Theme Token Display */}
      <section
        style={{
          padding: "16px",
          border: "1px solid var(--ui-border)",
          borderRadius: "var(--ui-radius-md)",
          background: "var(--ui-surface-alt)",
        }}
      >
        <h2 style={{ marginBottom: "12px" }}>Theme Tokens</h2>
        <pre
          style={{
            background: "var(--ui-surface)",
            padding: "12px",
            borderRadius: "var(--ui-radius-sm)",
            overflowX: "auto",
            fontSize: "0.85rem",
          }}
        >
{JSON.stringify(theme, null, 2)}
        </pre>
      </section>

      {/* Default Variant */}
      <TextInput
        label="Default Variant"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Type here..."
        variant="default"
      />

      {/* Ghost Variant */}
      <TextInput
        label="Ghost Variant"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Ghost input"
        variant="ghost"
      />

      {/* Solid Variant */}
      <TextInput
        label="Solid Variant"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Solid input"
        variant="solid"
      />

      {/* Underline Variant */}
      <TextInput
        label="Underline Variant"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Underline input"
        variant="underline"
      />

      {/* Compact Variant */}
      <TextInput
        label="Compact Variant"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Compact input"
        variant="compact"
      />

      {/* Error State */}
      <TextInput
        label="Error State Example"
        value={value}
        onChange={(e) => {
          const v = e.target.value;
          setValue(v);
          setError(v.length < 3 ? "Minimum 3 characters required" : "");
        }}
        placeholder="Triggers error under 3 chars"
        error={error}
        variant="default"
      />
    </div>
  );
}
