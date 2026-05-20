// /src/services/sessionEventBridge.js

import { pushSessionEvent } from "./sessionEventStream.js";

export function initSessionEventBridge() {
  const map = {
    "session-activity": "activity",
    "session-heartbeat": "heartbeat",
    "session-restore": "restore",
    "session-timeout": "timeout",
    "session-login": "login",
    "session-logout": "logout",
  };

  for (const domEvt in map) {
    window.addEventListener(domEvt, () => {
      pushSessionEvent(map[domEvt]);
    });
  }
}
