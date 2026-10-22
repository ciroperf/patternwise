export class EventBus {
  constructor() {
    this.handlers = new Map();
  }

  subscribe(event, handler) {
    if (!this.handlers.has(event)) this.handlers.set(event, []);
    this.handlers.get(event).push(handler);
  }

  publish(event, payload) {
    for (const handler of this.handlers.get(event) ?? []) handler(payload);
  }
}
