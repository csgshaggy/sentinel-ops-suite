import { logEvent } from "@/features/telemetry/telemetry";

export function logInfo(message, data = {}) {
  logEvent({
    level: "info",
    message,
    data,
    timestamp: Date.now(),
  });
}

export function logWarn(message, data = {}) {
  logEvent({
    level: "warn",
    message,
    data,
    timestamp: Date.now(),
  });
}

export function logError(message, data = {}) {
  logEvent({
    level: "error",
    message,
    data,
    timestamp: Date.now(),
  });
}

export function logDebug(message, data = {}) {
  if (import.meta.env.VITE_DEBUG_MODE === "true") {
    logEvent({
      level: "debug",
      message,
      data,
      timestamp: Date.now(),
    });
  }
}
