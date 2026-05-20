<script>
    import Chart from "$lib/charts/Chart.svelte";
    import {
        buildScoreLineChart,
        buildDriftBarChart,
        buildTimelineChart
    } from "$lib/charts/idrimCharts.js";

    import DiffViewer from "$lib/idrim/DiffViewer.svelte";
    import { formatDiffSection } from "$lib/idrim/diffUtils.js";

    export let data;

    // Backend-provided analysis
    let analysis = data?.analysis ?? null;
    let drift = analysis?.drift_events ?? [];
    let score = analysis?.integrity_score ?? null;

    // Temporary history until audit storage is added
    let history = [
        { timestamp: "T-3", score: 100 },
        { timestamp: "T-2", score: 95 },
        { timestamp: "T-1", score: 90 },
        { timestamp: "Now", score }
    ];

    // Diff state
    let diff = null;

    async function loadDiff() {
        const res = await fetch("/idrim/diff", {
            method: "POST",
            body: JSON.stringify({
                roles: analysis?.roles ?? {},
                permissions: analysis?.permissions ?? {},
                users: analysis?.users ?? {}
            }),
            headers: { "Content-Type": "application/json" }
        });

        if (res.ok) {
            const raw = await res.json();
            diff = {
                roles: formatDiffSection(raw.roles),
                permissions: formatDiffSection(raw.permissions),
                users: formatDiffSection(raw.users)
            };
        }
    }
</script>

<style>
    .page {
        padding: 2rem;
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }

    .header {
        font-size: 2rem;
        font-weight: 600;
    }

    .subheader {
        opacity: 0.7;
        margin-top: -0.5rem;
    }

    .grid {
        display: grid;
        grid-template-columns: 1fr 2fr;
        gap: 2rem;
    }

    .panel {
        background: var(--panel-bg);
        padding: 1.25rem;
        border-radius: 8px;
        box-shadow: var(--panel-shadow);
    }

    .score {
        font-size: 3rem;
        font-weight: bold;
        color: var(--accent-text);
    }

    .event {
        padding: 0.5rem 0;
        border-bottom: 1px solid var(--border);
    }

    .event:last-child {
        border-bottom: none;
    }

    button {
        padding: 0.5rem 1rem;
        background: var(--accent-bg);
        color: var(--accent-text);
        border: none;
        border-radius: 6px;
        cursor: pointer;
        margin-bottom: 1rem;
    }

    button:hover {
        opacity: 0.9;
    }
</style>

<div class="page">
    <div>
        <div class="header">IDRIM Analytics</div>
        <div class="subheader">Identity Drift & Role Integrity Monitoring — Deep Analysis</div>
    </div>

    <!-- Score + Drift Panels -->
    <div class="grid">
        <!-- Score Panel -->
        <div class="panel">
            <h2>Integrity Score</h2>
            <div class="score">{score ?? "—"}</div>

            <h3>Summary</h3>
            <p>
                {#if analysis}
                    {analysis.summary}
                {:else}
                    No analysis data loaded.
                {/if}
            </p>
        </div>

        <!-- Drift Events Panel -->
        <div class="panel">
            <h2>Drift Events</h2>

            {#if drift.length > 0}
                {#each drift as ev}
                    <div class="event">
                        <strong>{ev.event_type}</strong>
                        — {JSON.stringify(ev.details)}
                    </div>
                {/each}
            {:else}
                <p>No drift events detected.</p>
            {/if}
        </div>
    </div>

    <!-- Charts Section -->
    <div class="panel">
        <h2>Integrity Score Trend</h2>
        <Chart {...buildScoreLineChart(history)} />
    </div>

    <div class="panel">
        <h2>Drift Events by Type</h2>
        <Chart {...buildDriftBarChart(drift)} />
    </div>

    <div class="panel">
        <h2>Drift Timeline</h2>
        <Chart {...buildTimelineChart(drift)} />
    </div>

    <!-- Diff Viewer Section -->
    <div class="panel">
        <h2>Baseline vs Snapshot Diff</h2>

        <button on:click={loadDiff}>Generate Diff</button>

        {#if diff}
            <DiffViewer {diff} />
        {/if}
    </div>
</div>
