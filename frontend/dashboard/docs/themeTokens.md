# Sentinel Ops Suite — Theme Token Cheat Sheet

This cheat sheet documents the semantic design tokens used across the dashboard.

---

## 🎨 Colors

### Backgrounds
| Token | Tailwind Class | Description |
|-------|----------------|-------------|
| bg.base | bg-gray-800 / dark:bg-gray-950 | Primary app background |
| bg.panel | bg-gray-900 | Panel, card, sidebar background |
| bg.accent.blue | text-blue-400 / bg-blue-600 | Primary accent color |
| bg.accent.cyan | text-cyan-400 | Secondary accent |
| bg.accent.green | text-green-400 | Success |
| bg.accent.yellow | text-yellow-400 | Warning |
| bg.accent.red | text-red-400 | Critical |

### Status Colors
| Status | Class |
|--------|-------|
| Healthy | bg-green-600 |
| Warning | bg-yellow-600 |
| Critical | bg-red-600 |

---

## 🖋 Typography

| Token | Class | Usage |
|-------|--------|--------|
| h1 | text-3xl font-bold | Page titles |
| h2 | text-2xl font-bold | Section titles |
| h3 | text-xl font-semibold | Subsections |
| body | text-sm | Standard text |
| mono | font-mono text-xs | Logs, metrics, SSE streams |

---

## 📏 Spacing

| Token | Class | Usage |
|--------|--------|--------|
| page | p-6 | Page padding |
| panel | p-4 | Panel/card padding |
| gap | space-y-4 | Vertical spacing |

---

## 🧩 Components

### Cards
- `rounded-xl bg-ops-panel shadow-panel p-4`

### Panels
- `rounded-xl bg-ops-panel shadow-ops p-6`

### Buttons
- Primary: `px-4 py-2 rounded bg-blue-600 hover:bg-blue-500 text-white`
- Danger: `px-4 py-2 rounded bg-red-600 hover:bg-red-500 text-white`
- Ghost: `px-3 py-2 rounded hover:bg-gray-700`

---

## 🌙 Dark Mode

Dark mode is enabled via:

```html
<html class="dark">

Toggled by your ThemeToggle component.


---

# 🧩 2. Reusable Tailwind Component Classes  
**Path:**  

frontend/dashboard/styles/components.css


This gives you semantic utility classes you can apply anywhere.

```css
/* BUTTONS */
.btn {
  @apply px-4 py-2 rounded font-medium transition-colors;
}

.btn-primary {
  @apply btn bg-blue-600 hover:bg-blue-500 text-white;
}

.btn-danger {
  @apply btn bg-red-600 hover:bg-red-500 text-white;
}

.btn-ghost {
  @apply btn bg-transparent hover:bg-gray-700 dark:hover:bg-gray-800 text-gray-200;
}

/* CARDS */
.card {
  @apply rounded-xl bg-gray-900 dark:bg-gray-900 shadow-panel p-4;
}

.card-lg {
  @apply card p-6;
}

/* PANELS */
.panel {
  @apply rounded-xl bg-gray-900 dark:bg-gray-900 shadow-ops p-6;
}

/* BADGES */
.badge {
  @apply px-2 py-1 rounded text-xs font-semibold;
}

.badge-success {
  @apply badge bg-green-600 text-white;
}

.badge-warning {
  @apply badge bg-yellow-600 text-white;
}

.badge-critical {
  @apply badge bg-red-600 text-white;
}

/* INPUTS */
.input {
  @apply px-3 py-2 rounded bg-gray-900 border border-gray-700 text-gray-200;
}
