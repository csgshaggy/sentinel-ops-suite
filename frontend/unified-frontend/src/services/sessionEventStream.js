// /src/services/sessionEventStream.js

const listeners = new Set();
const events = [];

// Max events to keep in memory
const MAX_EVENTS = 200;

// ------------------------------------------------------------
// Add event to global buffer
// ------------------------------------------------------------
export function pushSessionEvent(type, payload = {}) {
  const evt = {
    ts: new Date().toISOString(),
    type,
    ...payload,
  };

  events.unshift(evt);
  if (events.length > MAX_EVENTS) events.pop();

  // Notify listeners
  for (const cb of listeners) cb(evt);
}

// ------------------------------------------------------------
// Subscribe to event stream
// ------------------------------------------------------------
export function subscribeToSessionEvents(callback) {
  listeners.add(callback);
  return () => listeners.delete(callback);
}

// ------------------------------------------------------------
// Get current buffer
// ------------------------------------------------------------
export function getSessionEventBuffer() {
  return [...events];
}
