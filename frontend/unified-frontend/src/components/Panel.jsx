import React, { memo } from "react";
import "../styles/theme.css";
import "../styles/global.css";
import "./Panel.css";

function Panel({ title, children }) {
  return (
    <div className="glass">
      {title && <div className="panel-header">{title}</div>}
      <div className="panel-content">{children}</div>
    </div>
  );
}

export default memo(Panel);
