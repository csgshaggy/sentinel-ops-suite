// frontend/src/lib/charts/idrimCharts.js

export function buildScoreLineChart(history) {
    return {
        type: "line",
        data: {
            labels: history.map(h => h.timestamp),
            datasets: [
                {
                    label: "Integrity Score",
                    data: history.map(h => h.score),
                    borderColor: "#4fd1c5",
                    tension: 0.25
                }
            ]
        }
    };
}

export function buildDriftBarChart(events) {
    const counts = {};

    for (const ev of events) {
        counts[ev.event_type] = (counts[ev.event_type] || 0) + 1;
    }

    return {
        type: "bar",
        data: {
            labels: Object.keys(counts),
            datasets: [
                {
                    label: "Drift Events",
                    data: Object.values(counts),
                    backgroundColor: "#63b3ed"
                }
            ]
        }
    };
}

export function buildTimelineChart(events) {
    return {
        type: "line",
        data: {
            labels: events.map(e => e.timestamp || "unknown"),
            datasets: [
                {
                    label: "Drift Timeline",
                    data: events.map((_, i) => i + 1),
                    borderColor: "#f6ad55",
                    tension: 0.25
                }
            ]
        }
    };
}
