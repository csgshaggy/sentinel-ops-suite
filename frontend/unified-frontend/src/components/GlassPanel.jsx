// /src/components/GlassPanel.jsx

import "./GlassPanel.css";
import "../styles/theme.css";

export default function GlassPanel({
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
