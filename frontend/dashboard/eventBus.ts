type Callback = (payload: any) => void;

class EventBus {
  private listeners: Record<string, Callback[]> = {};

  on(event: string, cb: Callback) {
    if (!this.listeners[event]) this.listeners[event] = [];
    this.listeners[event].push(cb);
  }

  off(event: string, cb: Callback) {
    this.listeners[event] = (this.listeners[event] || []).filter(
      (fn) => fn !== cb
    );
  }

  emit(event: string, payload?: any) {
    (this.listeners[event] || []).forEach((cb) => cb(payload));
  }
}

export const eventBus = new EventBus();
