// /src/components/skeletons/SkeletonLine.jsx
// SentinelOps — Skeleton Line (Neon‑Glassy)

import "./Skeletons.css";

export default function SkeletonLine({ width = "100%" }) {
  return (
    <div
      className="skeleton-line"
      style={{ width }}
    ></div>
  );
}
