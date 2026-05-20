# Dashboard Component Tree

## App Entry

- `AppRouter.tsx`
  - Wraps routes in `Layout`

## Layout Shell

- `Layout.tsx`
  - `MobileDrawer` (mobile nav)
  - `Nav` (sidebar navigation)
  - `StatusBar`
  - `CommandPalette`
  - `KeyboardShortcuts`
  - `NotificationCenter`
  - `OpsAlerts`
  - `Breadcrumbs`
  - `main` (routed content)

## Navigation

- `Nav.tsx`
  - Uses `navConfig.ts`

- `config/navConfig.ts`
  - Route metadata (name, path, icon, roles)

- `components/MobileDrawer.tsx`
  - Wraps `Nav` for mobile

## Global UX

- `components/StatusBar.tsx`
  - `ThemeToggle`

- `components/ThemeToggle.tsx`
- `components/CommandPalette.tsx`
- `components/KeyboardShortcuts.tsx`
- `components/NotificationCenter.tsx`
- `components/OpsAlerts.tsx`
- `components/Breadcrumbs.tsx`

## Pages

- `pages/DashboardHome.tsx`
  - SSE live metrics

- `pages/OpsConsole.tsx`
  - Unified PELM + IDRIM + Anomaly

- `pages/OpsTimeline.tsx`
- `pages/OpsHeatmap.tsx`
- `pages/OpsAssistant.tsx`

- `pages/PELMPanel.tsx`
- `pages/AnomalyPanel.tsx`
- `pages/IDRIMPanel.tsx`
- `pages/ValidatorPanel.tsx`
- `pages/RepoHealthPanel.tsx`
- `pages/GitHealthPanel.tsx`

## State & Events

- `eventBus.ts`
- `store/opsStore.ts`

## API

- `api/opsClient.ts`

