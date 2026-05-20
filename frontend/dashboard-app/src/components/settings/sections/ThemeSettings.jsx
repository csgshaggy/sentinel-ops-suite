import React from "react";

export default function ThemeSettings() {
  return (
    <>
      <div className="settings-item">
        <label htmlFor="themeMode">Theme mode</label>
        <select id="themeMode" className="settings-select">
          <option value="system">System Default</option>
          <option value="light">Light</option>
          <option value="dark">Dark</option>
        </select>
      </div>

      <div className="settings-item">
        <label htmlFor="accentColor">Accent color</label>
        <select id="accentColor" className="settings-select">
          <option value="blue">Blue</option>
          <option value="green">Green</option>
          <option value="purple">Purple</option>
          <option value="red">Red</option>
        </select>
      </div>
    </>
  );
}
