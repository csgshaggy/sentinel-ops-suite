<script>
    import { onMount } from "svelte";
    import { createIDRIMSSE } from "$lib/sse/idrimSSE.js";

    let driftEvents = [];
    let integrityScore = 100;

    onMount(() => {
        const sse = createIDRIMSSE((event) => {
            driftEvents = [event, ...driftEvents].slice(0, 20);
            integrityScore = Math.max(0, integrityScore - 5);
        });

        return () => sse.close();
    });
</script>

<style>
    .idrim-tile {
        padding: 1rem;
        border-radius: 8px;
        background: var(--panel-bg);
        box-shadow: var(--panel-shadow);
    }
    .score {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .event {
        padding: 0.25rem 0;
        border-bottom: 1px solid var(--border);
    }
</style>

<div class="idrim-tile">
    <div class="score">
        Integrity Score: {integrityScore}
    </div>

    <div>
        {#each driftEvents as ev}
            <div class="event">
                <strong>{ev.event_type}</strong>
                — {JSON.stringify(ev.details)}
            </div>
        {/each}
    </div>
</div>
