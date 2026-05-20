<script>
    export let diff = {};

    const colors = {
        added: "var(--green-500)",
        removed: "var(--red-500)",
        changed: "var(--yellow-500)"
    };
</script>

<style>
    .entry {
        padding: 0.5rem;
        border-bottom: 1px solid var(--border);
        font-family: monospace;
    }
    .key {
        font-weight: bold;
    }
</style>

<div>
    {#each Object.entries(diff) as [section, items]}
        <h3>{section}</h3>

        {#each items as item}
            <div class="entry" style="color: {colors[item.type]}">
                <span class="key">{item.key}</span> — {item.type}

                {#if item.type === "changed"}
                    <div>before: {JSON.stringify(item.before)}</div>
                    <div>after: {JSON.stringify(item.after)}</div>
                {:else}
                    <div>{JSON.stringify(item.value)}</div>
                {/if}
            </div>
        {/each}
    {/each}
</div>
