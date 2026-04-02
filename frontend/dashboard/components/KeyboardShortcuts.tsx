import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function KeyboardShortcuts() {
  const navigate = useNavigate();

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.shiftKey && e.key === "P") navigate("/pelm");
      if (e.shiftKey && e.key === "I") navigate("/idrim");
      if (e.shiftKey && e.key === "A") navigate("/anomaly");
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  return null;
}
