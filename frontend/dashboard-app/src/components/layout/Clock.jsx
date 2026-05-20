// src/components/layout/Clock.jsx

import { useEffect, useState } from "react";

const Clock = ({ use24h, showSeconds, showDay }) => {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  const options = {
    hour: "numeric",
    minute: "numeric",
    hour12: !use24h,
  };

  if (showSeconds) {
    options.second = "numeric";
  }

  if (showDay) {
    options.weekday = "long";
  }

  const formatted = new Intl.DateTimeFormat(undefined, options).format(now);

  return <div className="clock">{formatted}</div>;
};

export default Clock;

