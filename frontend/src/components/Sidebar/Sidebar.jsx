import React from "react";
import styles from "./Sidebar.module.css";
import { FiHome, FiSettings, FiFolder, FiChevronLeft } from "react-icons/fi";

export default function Sidebar({ collapsed, onToggle }) {
  return (
    <aside className={`${styles.sidebar} ${collapsed ? styles.collapsed : ""}`}>
      <div className={styles.logo}>
        <span>SentinelOps</span>
        <button
          className={styles.footerButton}
          onClick={onToggle}
          aria-label="Toggle sidebar"
        >
          <FiChevronLeft
            className={styles.icon}
            style={{ transform: collapsed ? "rotate(180deg)" : "none" }}
          />
        </button>
      </div>
      <nav className={styles.nav}>
        <div className={styles.sectionHeader}>Main</div>

        <div className={styles.navItem}>
          <FiHome className={styles.icon} />
          <span>Dashboard</span>
        </div>

        <div className={styles.navItem}>
          <FiFolder className={styles.icon} />
          <span>Projects</span>
        </div>
        <div className={styles.divider} />

        <div className={styles.sectionHeader}>System</div>

        <div className={styles.navItem}>
          <FiSettings className={styles.icon} />
          <span>Settings</span>
        </div>
      </nav>
      <footer className={styles.footer}>
        <button className={styles.footerButton}>
          <FiSettings className={styles.icon} />
          <span>Preferences</span>
        </button>

        <button className={styles.footerButton}>
          <FiFolder className={styles.icon} />
          <span>Storage</span>
        </button>
      </footer>
    </aside>
  );
}

