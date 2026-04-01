PELM_DASHBOARD_LAYOUT = {
    "panels": [
        {
            "id": "pelm-summary",
            "title": "PELM Summary",
            "type": "summary",
            "endpoint": "/pelm/summary",
        },
        {
            "id": "pelm-events",
            "title": "Recent PELM Events",
            "type": "event-table",
            "endpoint": "/pelm/events",
            "stream": "/pelm/events/stream",
        },
        {
            "id": "pelm-risks",
            "title": "Identity Risk Scores",
            "type": "risk-table",
            "endpoint": "/pelm/risks",
        },
        {
            "id": "pelm-graph",
            "title": "Lateral Movement Graph",
            "type": "graph",
            "endpoint": "/pelm/graph",
        },
    ]
}
