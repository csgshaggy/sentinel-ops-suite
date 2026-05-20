// frontend/src/lib/sse/idrimSSE.js

export function createIDRIMSSE(onEvent) {
    const source = new EventSource("/idrim/sse/drift");

    source.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            onEvent(data);
        } catch (err) {
            console.error("IDRIM SSE parse error:", err);
        }
    };

    source.onerror = (err) => {
        console.error("IDRIM SSE connection error:", err);
    };

    return source;
}
