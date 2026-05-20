<script>
    import { onMount } from "svelte";
    import Chart from "chart.js/auto";

    export let type;
    export let data;
    export let options = {};

    let canvas;

    onMount(() => {
        const chart = new Chart(canvas, {
            type,
            data,
            options
        });

        return () => chart.destroy();
    });
</script>

<canvas bind:this={canvas}></canvas>
