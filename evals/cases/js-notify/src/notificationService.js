import { NotifierFactory } from "./notifiers.js";
import { getRetryPolicy } from "./retryPolicies.js";
import { EventBus } from "./eventBus.js";
import { AuditLog, AuditLogProxy } from "./auditLog.js";

export function createNotificationService({ transport, retry = "fixed", sleep = async () => {} }) {
  const notifier = new NotifierFactory().createNotifier(transport);
  const policy = getRetryPolicy(retry);
  const audit = new AuditLogProxy(new AuditLog());
  const bus = new EventBus();
  bus.subscribe("notification.sent", (e) => audit.record(e));

  async function notify(to, message) {
    for (let attempt = 1; ; attempt++) {
      try {
        await notifier.send(to, message);
        bus.publish("notification.sent", { to, channel: notifier.getChannelName(), attempt });
        return { ok: true, attempts: attempt };
      } catch (err) {
        const delay = policy(attempt);
        if (delay === null) return { ok: false, attempts: attempt, error: err.message };
        await sleep(delay);
      }
    }
  }

  return { notify, audit };
}
