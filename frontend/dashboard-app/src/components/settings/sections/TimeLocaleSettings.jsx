import React from "react";

export default function TimeLocaleSettings() {
  return (
    <>
      <div className="settings-item">
        <label htmlFor="use24h">Use 24-hour clock format</label>
        <input id="use24h" type="checkbox" className="settings-checkbox" />
      </div>

      <div className="settings-item">
        <label htmlFor="showSeconds">Show seconds on clock</label>
        <input id="showSeconds" type="checkbox" className="settings-checkbox" />
      </div>

      <div className="settings-item">
        <label htmlFor="showDayOfWeek">Show day of week in TopBar</label>
        <input id="showDayOfWeek" type="checkbox" className="settings-checkbox" />
      </div>

      <div className="settings-item">
        <label htmlFor="timezone">Timezone</label>
        <select id="timezone" className="settings-select">
          <option value="local">System Default</option>
          <option value="utc">UTC</option>
        </select>
      </div>
    </>
  );
}
