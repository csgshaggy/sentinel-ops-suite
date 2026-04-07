export function setTheme(theme) {
  if (!["light", "dark"].includes(theme)) return;
  document.documentElement.setAttribute("data-theme", theme);
}

export function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  setTheme(next);
}

export function initTheme() {
  const existing = document.documentElement.getAttribute("data-theme");
  if (!existing) setTheme("dark");
}
