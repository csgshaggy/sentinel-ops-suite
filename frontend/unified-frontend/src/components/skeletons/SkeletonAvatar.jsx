// /src/components/skeletons/SkeletonAvatar.jsx
// SentinelOps — Skeleton Avatar (Circle Placeholder)

import "./Skeletons.css";

export default function SkeletonAvatar({ size = 80 }) {
  return (
    <div
      className="skeleton-avatar"
      style={{ width: size, height: size }}
    ></div>
  );
}
