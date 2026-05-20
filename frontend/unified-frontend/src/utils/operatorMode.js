// /src/utils/operatorMode.js

const STORAGE_KEY = "operator_mode_enabled";

/**
 * Returns true if operator mode is enabled.
 */
export function isOperatorMode() {
  try {
    return localStorage.getItem(STORAGE_KEY) === "true";
  } catch {
    return false;
  }
}

/**
 * Enables operator mode.
 */
export function enableOperatorMode() {
  try {
    localStorage.setItem(STORAGE_KEY, "true");
    emitChangeEvent(true);
  } catch {}
}

/**
 * Disables operator mode.
 */
export function disableOperatorMode() {
  try {
    localStorage.setItem(STORAGE_KEY, "false");
    emitChangeEvent(false);
  } catch {}
}

/**
 * Toggles operator mode.
 */
export function toggleOperatorMode() {
  const newValue = !isOperatorMode();
  try {
    localStorage.setItem(STORAGE_KEY, newValue ? "true" : "false");
    emitChangeEvent(newValue);
  } catch {}
}

/**
 * Emits a custom event so components can react.
 */
function emitChangeEvent(enabled) {
  window.dispatchEvent(
    new CustomEvent("operatorModeChanged", {
      detail: { enabled },
    })
  );
}
