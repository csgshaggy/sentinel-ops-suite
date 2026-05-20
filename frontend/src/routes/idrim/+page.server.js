// frontend/src/routes/idrim/+page.server.js

/**
 * Server-side loader for the /idrim analytics page.
 * Fetches a fresh IDRIM analysis snapshot.
 */

export async function load({ fetch }) {
    let analysis = null;

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
            analysis = await res.json();
        }
    } catch (err) {
        console.error("IDRIM /idrim preload failed:", err);
    }

    return {
        analysis
    };
}
