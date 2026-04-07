// frontend/src/routes/dashboard/+page.server.js

/** 
 * Server-side loader for the dashboard.
 * This runs on the server before the page renders.
 * 
 * It can fetch:
 *   • IDRIM integrity score
 *   • Recent drift events
 *   • System health
 *   • PELM metrics
 * 
 * All values are optional and safe to extend later.
 */

export async function load({ fetch }) {
    // Fetch IDRIM analysis (optional — safe fallback)
    let idrim = null;
    try {
        const res = await fetch("/idrim/analysis", {
            method: "POST",
            body: JSON.stringify({
                roles: {},
                permissions: {},
                users: {}
            }),
            headers: { "Content-Type": "application/json" }
        });

        if (res.ok) {
            idrim = await res.json();
        }
    } catch (err) {
        console.error("IDRIM preload failed:", err);
    }

    // Fetch system health (optional)
    let system = null;
    try {
        const res = await fetch("/system/health");
        if (res.ok) {
            system = await res.json();
        }
    } catch (err) {
        console.error("System preload failed:", err);
    }

    return {
        idrim,
        system
    };
}
