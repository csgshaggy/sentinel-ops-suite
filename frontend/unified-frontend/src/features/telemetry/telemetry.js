// /src/features/telemetry/telemetry.js

import { v4 as uuidv4 } from "uuid";

const buildVersion = import.meta.env.VITE_APP_BUILD_VERSION || "dev";

/**
 * Base metadata attached to every telemetry event.
 */
function getBaseMeta(component) {
  return {
    sessionId: localStorage.getItem("sessionId") || null,
    userId: localStorage.getItem("userId") || null,
    component: component || "unknown",
    version: buildVersion,
  };
}

/**
 * Core low-level emitter used by Telemetry.* helpers.
 */
export function emitTelemetry(event, level = "info", context = {}, component = null) {
  try {
    const payload = {
      event,
      level,
      timestamp: Date.now(),
      context,
      meta: getBaseMeta(component),
    };

    // Local dev: console output
    if (import.meta.env.DEV) {
      console.log("[telemetry]", payload);
    }

    // Backend ingestion
    fetch("/api/telemetry/ingest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).catch(() => {
      // Telemetry must never break UX
    });

    return payload;
  } catch (err) {
    console.error("Telemetry emit failed:", err);
  }
}

/**
 * High-level logger integration point.
 * logger.js calls this directly.
 */
export function logEvent({ level = "info", message, data = {}, timestamp = Date.now(), component = null }) {
  try {
    const payload = {
      event: message,        // logger uses "message" as event name
      level,
      timestamp,
      context: data,
      meta: getBaseMeta(component),
    };

    if (import.meta.env.DEV) {
      console.log("[telemetry:logEvent]", payload);
    }

    fetch("/api/telemetry/ingest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).catch(() => {});

    return payload;
  } catch (err) {
    console.error("logEvent failed:", err);
  }
}

/**
 * Event-family helpers (optional but recommended).
 * These wrap emitTelemetry() with deterministic naming.
 */
export const Telemetry = {
  session: (event, context = {}, component = null) =>
    emitTelemetry(`session.${event}`, "info", context, component),

  heartbeat: (event, context = {}, component = null) =>
    emitTelemetry(`heartbeat.${event}`, "info", context, component),

  api: (event, context = {}, component = null, level = "error") =>
    emitTelemetry(`api.${event}`, level, context, component),

  ui: (event, context = {}, component = null) =>
    emitTelemetry(`ui.${event}`, "info", context, component),

  perf: (event, context = {}, component = null) =>
    emitTelemetry(`perf.${event}`, "info", context, component),

  sec: (event, context = {}, component = null, level = "warn") =>
    emitTelemetry(`sec.${event}`, level, context, component),
};

