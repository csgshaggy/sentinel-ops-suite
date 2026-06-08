// /src/components/skeletons/SkeletonTable.jsx
// SentinelOps — Skeleton Table (Rows + Columns)

import SkeletonLine from "./SkeletonLine.jsx";
import "./Skeletons.css";

export default function SkeletonTable({ rows = 3, cols = 4 }) {
  return (
    <div className="skeleton-table glass">
      {[...Array(rows)].map((_, r) => (
        <div key={r} className="skeleton-table-row">
          {[...Array(cols)].map((_, c) => (
            <SkeletonLine key={c} width={`${70 - c * 10}%`} />
          ))}
        </div>
      ))}
    </div>
  );
}
