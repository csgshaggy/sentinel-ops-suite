// /src/components/apiErrorBus.js
// Simple event bus for API errors

let listeners = [];

export function emitApiError(payload) {
  listeners.forEach((cb) => cb(payload));
}

export function subscribeApiError(cb) {
  listeners.push(cb);
  return () => {
    listeners = listeners.filter((fn) => fn !== cb);
  };
}
