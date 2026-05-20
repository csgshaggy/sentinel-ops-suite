import React from "react";

export default function FormRow({ children, className = "" }) {
  return (
    <div className={`ui-form-row ${className}`}>
      {children}
    </div>
  );
}
