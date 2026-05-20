import React from "react";

export default function Form({ children, onSubmit, className = "" }) {
  return (
    <form
      onSubmit={onSubmit}
      className={`ui-form ${className}`}
      noValidate
    >
      {children}
    </form>
  );
}
