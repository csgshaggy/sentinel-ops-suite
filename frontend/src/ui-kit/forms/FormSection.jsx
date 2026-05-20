import React from "react";

export default function FormSection({ title, children, className = "" }) {
  return (
    <div className={`ui-form-section ${className}`}>
      {title && <h3 className="ui-form-section-title">{title}</h3>}
      <div className="ui-form-section-body">{children}</div>
    </div>
  );
}
