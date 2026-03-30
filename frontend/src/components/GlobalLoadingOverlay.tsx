// =====================================================================
// SSRF Command Console — Global Loading Overlay
// Driven by LayoutContext.globalLoading
// =====================================================================

import { useLayout } from "../context/LayoutContext";

export default function GlobalLoadingOverlay() {
  const { globalLoading } = useLayout();

  if (!globalLoading) return null;

  return (
    <div className="global-loading-overlay">
      <div className="global-loading-spinner">
        <div className="spinner-dot" />
        <div className="spinner-dot" />
        <div className="spinner-dot" />
      </div>
    </div>
  );
}
