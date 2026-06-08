// /src/components/skeletons/SkeletonBlock.jsx
// SentinelOps — Skeleton Block (Card / Panel Placeholder)

import "./Skeletons.css";

export default function SkeletonBlock({ height = "120px" }) {
  return (
    <div
      className="skeleton-block"
      style={{ height }}
    ></div>
  );
}
