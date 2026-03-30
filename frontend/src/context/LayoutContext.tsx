// =====================================================================
// SSRF Command Console — LayoutContext
// Sidebar collapse • Breadcrumbs • Global loading overlay
// =====================================================================

import { createContext, useContext, useState, ReactNode, useCallback } from "react";

export type Breadcrumb = {
  label: string;
  path: string;
};

type LayoutContextType = {
  sidebarCollapsed: boolean;
  setSidebarCollapsed: (v: boolean) => void;

  breadcrumbs: Breadcrumb[];
  setBreadcrumbs: (b: Breadcrumb[]) => void;

  globalLoading: boolean;
  setGlobalLoading: (v: boolean) => void;
};

const LayoutContext = createContext<LayoutContextType | undefined>(undefined);

export function LayoutProvider({ children }: { children: ReactNode }) {
  const [sidebarCollapsed, setSidebarCollapsedState] = useState(false);
  const [breadcrumbs, setBreadcrumbsState] = useState<Breadcrumb[]>([]);
  const [globalLoading, setGlobalLoadingState] = useState(false);

  const setSidebarCollapsed = useCallback((v: boolean) => {
    setSidebarCollapsedState(v);
  }, []);

  const setBreadcrumbs = useCallback((b: Breadcrumb[]) => {
    setBreadcrumbsState(b);
  }, []);

  const setGlobalLoading = useCallback((v: boolean) => {
    setGlobalLoadingState(v);
  }, []);

  return (
    <LayoutContext.Provider
      value={{
        sidebarCollapsed,
        setSidebarCollapsed,

        breadcrumbs,
        setBreadcrumbs,

        globalLoading,
        setGlobalLoading,
      }}
    >
      {children}
    </LayoutContext.Provider>
  );
}

export function useLayout() {
  const ctx = useContext(LayoutContext);
  if (!ctx) {
    throw new Error("useLayout must be used within LayoutProvider");
  }
  return ctx;
}
