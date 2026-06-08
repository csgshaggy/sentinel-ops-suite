// /src/components/SessionEventTimeline.jsx

import { useEffect, useState } from "react";

const BUS = "session-event";
const MAX_EVENTS = 100;

export default function SessionEventTimeline() {
  const [events, setEvents] = useState([]);
  const [visible, setVisible] = useState(false);

  // Toggle: Ctrl + Shift + T
  useEffect(() => {
    const handler = (e) => {
      if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === "t") {
        setVisible((v) => !v);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  // Listen for session events from logSessionEvent()
  useEffect(() => {
    const listener = (e) => {
      setEvents((prev) => {
        const next = [e.detail, ...prev];
        return next.slice(0, MAX_EVENTS);
      });
    };

    window.addEventListener(BUS, listener);
    return () => window.removeEventListener(BUS, listener);
  }, []);

  if (!visible) return null;

  return (
    <div
      style={{
        position: "fixed",
        bottom: 20,
        left: 20,
        width: 420,
        maxHeight: 320,
        overflowY: "auto",
        background: "rgba(0,0,0,0.9)",
        color: "white",
        fontFamily: "monospace",
        fontSize: 11,
        padding: 12,
        borderRadius: 8,
        zIndex: 99998,
      }}
    >
      <div style={{ fontWeight: "bold", marginBottom: 8 }}>
        SESSION EVENT TIMELINE (Ctrl+Shift+T)
      </div>

      {events.map((ev, idx) => (
        <div key={idx} style={{ marginBottom: 4 }}>
          <span style={{ opacity: 0.6 }}>{ev.ts}</span>{" "}
          <span style={{ fontWeight: "bold" }}>{ev.event}</span>{" "}
          <span style={{ opacity: 0.8 }}>
            {JSON.stringify(ev).replace(/^{|}$/g, "")}
          </span>
        </div>
      ))}
    </div>
  );
}
