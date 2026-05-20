import { useEffect, useRef } from "react";

export function useInactivityTimer(timeoutMs, onTimeout) {
  const timerRef = useRef(null);

  // Reset inactivity timer
  const resetTimer = () => {
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(onTimeout, timeoutMs);
  };

  useEffect(() => {
    // Activity events that count as "user is active"
    const events = ["mousemove", "keydown", "click", "scroll"];

    events.forEach((event) => {
      window.addEventListener(event, resetTimer);
    });

    // Start initial timer
    resetTimer();

    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
      events.forEach((event) => {
        window.removeEventListener(event, resetTimer);
      });
    };
  }, [timeoutMs, onTimeout]);
}
