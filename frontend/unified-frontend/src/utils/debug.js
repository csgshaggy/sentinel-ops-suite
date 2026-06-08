export const DEBUG_MODE =
  import.meta.env.VITE_DEBUG_MODE === "true";

export function debugLog(...args) {
  if (DEBUG_MODE) {
    console.log("[DEBUG]", ...args);
  }
}
