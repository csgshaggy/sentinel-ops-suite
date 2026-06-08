// /src/components/GlassPanel.jsx

import React, { memo } from "react";
import "./GlassPanel.css";
import "../styles/theme.css";

function GlassPanel({
  children,
  className = "",
  padding = "20px",
  radius = "var(--radius)",
  shadow = "var(--neon-glow)",
  style = {},
  ...rest
}) {
  return (
    <div
      className={`glass-panel ${className}`}
      style={{
        padding,
        borderRadius: radius,
        boxShadow: shadow,
        ...style,
      }}
      {...rest}
    >
      {children}
    </div>
  );
}

export default memo(GlassPanel);
