import React from "react";

export default function FormActions({ children, className = "" }) {
  return (
    <div className={`ui-form-actions ${className}`}>
      {children}
    </div>
  );
}
