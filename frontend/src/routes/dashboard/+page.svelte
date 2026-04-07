<script>
    import PELMTile from "./tiles/PELMTile.svelte";
    import SystemTile from "./tiles/SystemTile.svelte";
    import IDRIMTile from "./tiles/IDRIMTile.svelte";
</script>

<style>
    .dashboard-container {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        padding: 1.5rem;
    }

    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 1.5rem;
    }

    .header {
        font-size: 1.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .subheader {
        font-size: 1rem;
        opacity: 0.7;
        margin-bottom: 1rem;
    }
</style>

<div class="dashboard-container">
    <div>
        <div class="header">Sentinel Ops Dashboard</div>
        <div class="subheader">Operational health, integrity monitoring, and real‑time drift detection</div>
    </div>

    <div class="dashboard-grid">
        <PELMTile />
        <SystemTile />
        <IDRIMTile />
    </div>
</div>
