// frontend/src/lib/shortcuts/idrimShortcut.js

import { goto } from "$app/navigation";

/**
 * Registers a keyboard shortcut for jumping to the IDRIM tile.
 * Default combo: g then i (pressed sequentially, not held).
 */

export function registerIDRIMShortcut() {
    let buffer = [];

    const handler = (e) => {
        buffer.push(e.key.toLowerCase());

        // Keep buffer small
        if (buffer.length > 2) buffer.shift();

        // Match sequence: g then i
        if (buffer.join("") === "gi") {
            goto("/dashboard?panel=idrim");
            buffer = [];
        }
    };

    window.addEventListener("keydown", handler);

    return () => {
        window.removeEventListener("keydown", handler);
    };
}
