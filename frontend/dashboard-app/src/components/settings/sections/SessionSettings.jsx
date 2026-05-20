import React from "react";

export default function SessionSettings() {
  return (
    <>
      <div className="settings-item">
        <label htmlFor="sessionTimeout">Session timeout (minutes)</label>
        <select id="sessionTimeout" className="settings-select">
          <option value="5">5</option>
          <option value="10">10</option>
          <option value="15">15</option>
          <option value="30">30</option>
        </select>
      </div>

      <div className="settings-item">
        <label htmlFor="warnBeforeTimeout">Show expiration warning</label>
        <input id="warnBeforeTimeout" type="checkbox" className="settings-checkbox" />
      </div>

      <div className="settings-item">
        <label htmlFor="autoExtend">Allow “Stay Logged In” extension</label>
        <input id="autoExtend" type="checkbox" className="settings-checkbox" />
      </div>
    </>
  );
}
