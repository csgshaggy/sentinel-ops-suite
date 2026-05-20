import React, { useState, useRef, useEffect } from "react";

export default function SettingsSection({ title, children, defaultOpen = true }) {
  const [open, setOpen] = useState(defaultOpen);
  const bodyRef = useRef(null);
  const [height, setHeight] = useState("auto");

  // Measure height for smooth animation
  useEffect(() => {
    if (bodyRef.current) {
      setHeight(open ? `${bodyRef.current.scrollHeight}px` : "0px");
    }
  }, [open, children]);

  return (
    <div className="settings-section">
      {/* Header */}
      <div className="settings-section-header" onClick={() => setOpen(!open)}>
        <h3 className="settings-section-title">{title}</h3>
        <span className={`collapse-arrow ${open ? "open" : ""}`}>▸</span>
      </div>

      {/* Collapsible Body */}
      <div
        className="settings-section-body-wrapper"
        style={{
          height,
          overflow: "hidden",
          transition: "height 0.25s ease",
        }}
      >
        <div ref={bodyRef} className="settings-section-body">
          {children}
        </div>
      </div>
    </div>
  );
}
