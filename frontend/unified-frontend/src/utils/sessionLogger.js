// /src/utils/sessionLogger.js

const SESSION_EVENT_BUS = "session-event";

export function logSessionEvent(event, data = {}) {
  const payload = {
    ts: new Date().toISOString(),
    event,
    ...data,
  };

  // Structured JSON log for console + backend mirroring

  // Emit event for operator UI components
  window.dispatchEvent(
    new CustomEvent(SESSION_EVENT_BUS, { detail: payload })
  );
}
