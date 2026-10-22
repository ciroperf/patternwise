import { test } from "node:test";
import assert from "node:assert/strict";
import { createNotificationService } from "../src/notificationService.js";
import { retryPolicies } from "../src/retryPolicies.js";

function flakyTransport(failures) {
  let calls = 0;
  return {
    deliver() {
      calls++;
      if (calls <= failures) throw new Error("smtp down");
    },
  };
}

test("sends and records an audit entry", async () => {
  const svc = createNotificationService({ transport: flakyTransport(0) });
  assert.deepEqual(await svc.notify("a@b.c", "hi"), { ok: true, attempts: 1 });
  assert.deepEqual(svc.audit.all(), [{ to: "a@b.c", channel: "email", attempt: 1, at: 0 }]);
});

test("retries with fixed policy then succeeds", async () => {
  const delays = [];
  const svc = createNotificationService({
    transport: flakyTransport(2),
    sleep: async (ms) => delays.push(ms),
  });
  assert.deepEqual(await svc.notify("a@b.c", "hi"), { ok: true, attempts: 3 });
  assert.deepEqual(delays, [100, 100]);
});

test("gives up with no-retry policy", async () => {
  const svc = createNotificationService({ transport: flakyTransport(1), retry: "none" });
  assert.deepEqual(await svc.notify("a@b.c", "hi"), { ok: false, attempts: 1, error: "smtp down" });
  assert.equal(svc.audit.count(), 0);
});

test("exponential policy doubles delays", () => {
  assert.deepEqual([1, 2, 3, 4, 5].map((n) => retryPolicies.exponential(n)), [50, 100, 200, 400, null]);
});

test("unknown policy is rejected", () => {
  assert.throws(() => createNotificationService({ transport: {}, retry: "bogus" }), /Unknown retry policy/);
});
