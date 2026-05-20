import React from "react";

export interface TimingBucket {
  start: number;
  end: number;
  count: number;
  label: string;
}

interface TimingHeatMapProps {
  buckets: TimingBucket[];
}

const TimingHeatMap: React.FC<TimingHeatMapProps> = ({ buckets }) => {
  return (
    <div className="timing-heatmap">
      {buckets.map((b) => (
        <div key={b.label} className="timing-bucket">
          <div>{b.label}</div>
          <div className="timing-bar" style={{ width: `${b.count}px` }} />
        </div>
      ))}
    </div>
  );
};

export default TimingHeatMap;
