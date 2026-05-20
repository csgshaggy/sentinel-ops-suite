import { useEffect } from "react";

export default function useAutoRefresh(callback: () => void, intervalMs: number) {
  useEffect(() => {
    const id = setInterval(callback, intervalMs);
    return () => clearInterval(id);
  }, [callback, intervalMs]);
}
