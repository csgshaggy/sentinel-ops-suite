// /src/components/SentinelFooter.jsx

import React, { memo } from "react";
import "./SentinelFooter.css";
import version from "../version";

function SentinelFooter() {
  return (
    <footer className="sentinel-footer">
      <span className="footer-text">
        Sentinel Ops Suite
      </span>

      <span className="footer-version">
        v{version}
      </span>
    </footer>
  );
}

export default memo(SentinelFooter);
