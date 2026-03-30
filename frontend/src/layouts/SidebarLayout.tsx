import { useTheme } from "../context/ThemeContext";
import "./SidebarLayout.css";

export default function SidebarLayout({ children }: { children: React.ReactNode }) {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="layout">
      <aside className="sidebar">
        <button className="theme-toggle" onClick={toggleTheme}>
          {theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode"}
        </button>
      </aside>

      <main className="content">{children}</main>
    </div>
  );
}
