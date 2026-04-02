import React from "react";

interface TotpInputProps {
  value: string;
  onChange: (v: string) => void;
}

export default function TotpInput({ value, onChange }: TotpInputProps) {
  return (
    <input
      type="text"
      inputMode="numeric"
      maxLength={6}
      placeholder="123456"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      style={{
        fontSize: "1.2rem",
        padding: "0.5rem",
        width: "120px",
        textAlign: "center",
        letterSpacing: "0.2rem",
      }}
    />
  );
}
