// /src/main.jsx

import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./App.jsx";
import { AuthProvider } from "./features/auth/AuthContext.jsx";
import GlobalErrorBoundary from "./components/GlobalErrorBoundary.jsx";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

import { logEvent } from "./features/telemetry/telemetry.js";

import "./styles/theme.css";
import "./styles/global.css";
import "./styles/session-expire.css";

// ------------------------------------------------------------
// GLOBAL QUERY CLIENT
// ------------------------------------------------------------
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error) => {
        if (error?.response?.status >= 400 && error?.response?.status < 500) {
          return false;
        }
        return failureCount < 2;
      },
      retryDelay: (attemptIndex) =>
        Math.min(1000 * 2 ** attemptIndex, 8000),

      staleTime: 30_000,
      cacheTime: 5 * 60_000,
      refetchOnWindowFocus: false,
      refetchOnReconnect: true,
      refetchOnMount: false,
    },
    mutations: {
      retry: false,
    },
  },
});

// ------------------------------------------------------------
// TELEMETRY PIPELINE
// ------------------------------------------------------------
queryClient.getQueryCache().subscribe((event) => {
  if (event?.type === "query" && event.query.state.status === "error") {
    logEvent({
      type: "react-query.query-error",
      key: event.query.queryKey,
      error: event.query.state.error,
      timestamp: Date.now(),
    });
  }
});

queryClient.getMutationCache().subscribe((event) => {
  if (event?.type === "mutation" && event.mutation.state.status === "error") {
    logEvent({
      type: "react-query.mutation-error",
      key: event.mutation.options.mutationKey,
      error: event.mutation.state.error,
      timestamp: Date.now(),
    });
  }
});

// ------------------------------------------------------------
// ROOT RENDER — BrowserRouter moved to the top
// ------------------------------------------------------------
ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <GlobalErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <App />

          {import.meta.env.VITE_ENABLE_RQ_DEVTOOLS === "true" && (
            <ReactQueryDevtools initialIsOpen={false} />
          )}
        </AuthProvider>
      </QueryClientProvider>
    </GlobalErrorBoundary>
  </BrowserRouter>
);
