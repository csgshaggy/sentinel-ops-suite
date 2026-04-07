import React from "react";
import { TextInput, Theme } from "@/ui-kit";

export default function UiKitTest() {
  return (
    <div style={{
      padding: "40px",
      maxWidth: "420px",
      margin: "0 auto",
      display: "flex",
      flexDirection: "column",
      gap: "20px"
    }}>
      
      <h1>UI Kit Test</h1>

      <TextInput label="Username" placeholder="Type here..." />
      <TextInput label="Password" type="password" placeholder="••••••••" />
      <TextInput label="Error Example" error="Invalid input" />

      <button
        onClick={() => Theme.toggleTheme()}
        style={{
          marginTop: "20px",
          padding: "10px 16px",
          borderRadius: "6px",
          border: "1px solid #999",
          cursor: "pointer"
        }}
      >
        Toggle Theme
      </button>
    </div>
  );
}
