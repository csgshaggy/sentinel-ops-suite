// /src/components/GlobalErrorBoundary.jsx

import { ErrorBoundary } from "react-error-boundary";
import ErrorFallback from "./ErrorFallback.jsx";

export default function GlobalErrorBoundary({ children }) {
  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onReset={() => {
        window.location.reload();
      }}
    >
      {children}
    </ErrorBoundary>
  );
}
