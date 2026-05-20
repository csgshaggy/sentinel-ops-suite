<script lang="ts">
  import { onMount } from "svelte";

  let loading = true;
  let running = false;
  let error: string | null = null;

  let baselineExists: boolean = false;
  let hasLastRun: boolean = false;
  let integrityScore: number | null = null;
  let drift: any = null;
  let timestamp: string | null = null;

  async function loadSummary() {
    loading = true;
    error = null;

    try {
      const res = await fetch("/dashboard/idrim/summary");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      baselineExists = data.baseline_exists;
      hasLastRun = data.has_last_run;
      integrityScore = data.integrity_score;
      drift = data.drift;
      timestamp = data.timestamp;
    } catch (err: any) {
      error = err.message;
    } finally {
      loading = false;
    }
  }

  async function runIDRIM() {
    running = true;
    error = null;

    try {
      const res = await fetch("/dashboard/idrim/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          source: "dashboard",
          scope: "manual",
          payload: {}
        })
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const result = await res.json();

      integrityScore = result.integrity_score;
      drift = result.drift;
      timestamp = result.timestamp;
      hasLastRun = true;
    } catch (err: any) {
      error = err.message;
    } finally {
      running = false;
    }
  }

  onMount(loadSummary);
</script>

<style>
  .tile {
    padding: 1rem;
    border-radius: 8px;
    background: var(--surface-1);
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .score {
    font-size: 2rem;
    font-weight: 600;
  }

  .drift {
    font-family: monospace;
    font-size: 0.9rem;
    white-space: pre-wrap;
  }

  button {
    padding: 0.5rem 1rem;
    border-radius: 6px;
    background: var(--accent);
    color: white;
    border: none;
    cursor: pointer;
  }

  button:disabled {
    opacity: 0.5;
    cursor: default;
  }
</style>

<div class="tile">
  {#if loading}
    <div>Loading IDRIM status…</div>
  {:else if error}
    <div style="color: var(--error)">Error: {error}</div>
  {:else}
    <div>
      <strong>Baseline:</strong>
      {baselineExists ? "Present" : "Not Set"}
    </div>

    {#if hasLastRun}
      <div class="score">
        Integrity: {integrityScore}
      </div>

      {#if drift}
        <div class="drift">
          {JSON.stringify(drift, null, 2)}
        </div>
      {/if}

      <div>
        <small>Last run: {timestamp}</small>
      </div>
    {:else}
      <div>No previous IDRIM run.</div>
    {/if}

    <button on:click={runIDRIM} disabled={running}>
      {running ? "Running…" : "Run IDRIM"}
    </button>
  {/if}
</div>
