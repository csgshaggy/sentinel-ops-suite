// /src/utils/sessionMetrics.js

const metrics = {
  heartbeatCount: 0,
  lastHeartbeatTs: null,
  avgHeartbeatIntervalMs: null,

  lastActivityTs: null,

  restoreCount: 0,
  lastRestoreTs: null,

  lastHeartbeatDurationMs: null,
  lastHeartbeatStart: null,
};

export function recordHeartbeat() {
  const now = Date.now();

  // Track intervals
  if (metrics.lastHeartbeatTs) {
    const prev = new Date(metrics.lastHeartbeatTs).getTime();
    const interval = now - prev;

    if (!metrics.avgHeartbeatIntervalMs) {
      metrics.avgHeartbeatIntervalMs = interval;
    } else {
      metrics.avgHeartbeatIntervalMs =
        (metrics.avgHeartbeatIntervalMs * 0.8) + (interval * 0.2);
    }
  }

  metrics.heartbeatCount += 1;
  metrics.lastHeartbeatTs = new Date(now).toISOString();
}

export function recordActivity() {
  metrics.lastActivityTs = new Date().toISOString();
}

export function recordRestore() {
  metrics.restoreCount += 1;
  metrics.lastRestoreTs = new Date().toISOString();
}

export function getSessionMetrics() {
  return { ...metrics };
}
