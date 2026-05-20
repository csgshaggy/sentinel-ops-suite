// /src/components/toastBus.js

export const toast = {
  listeners: [],
  send(type, message, duration = 4000) {
    this.listeners.forEach((cb) => cb({ type, message, duration }));
  },
  success(msg, duration) {
    this.send("success", msg, duration);
  },
  error(msg, duration) {
    this.send("error", msg, duration);
  },
  warning(msg, duration) {
    this.send("warning", msg, duration);
  },
  info(msg, duration) {
    this.send("info", msg, duration);
  },
};
