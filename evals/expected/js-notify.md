# Answer key – js-notify (Node ESM, tests present)

Test command: `npm test` (5 tests, all green). No dependencies.

This case mainly measures the ability **not** to invent patterns and to recognize
**over-engineering**.

## Patterns – expected verdict
| Element | Where | Expected verdict |
|---|---|---|
| `retryPolicies` + `getRetryPolicy` | src/retryPolicies.js | **Sound Strategy** (idiomatic: map of functions, 3 real variants, chosen by config, tested). Must not be turned into classes. |
| `INotifier` | src/notifiers.js | **Over-engineered** (Speculative Generality): abstract "interface" with one implementation. Remedy: Collapse Hierarchy. |
| `AbstractNotifierFactory` + `NotifierFactory` | src/notifiers.js | **Over-engineered**: abstract factory with one product and one family; not a real Abstract Factory. Remedy: Inline Class/Method → `new EmailNotifier(transport)`. |
| `EventBus` | src/eventBus.js + notificationService.js | **Over-engineered**: one publisher and one subscriber wired in the same function; the flow becomes opaque. Remedy: direct call `audit.record(...)`. Acceptable if the skill says to keep it only when more real subscribers are expected. |
| `AuditLogProxy` | src/auditLog.js | **Name only / Middle Man**: forwards everything without control. Remedy: Remove Middle Man. |

## Expected smells
- Speculative Generality (INotifier, AbstractNotifierFactory) – Medium
- Middle Man (AuditLogProxy) – Medium/Low
- Lazy Class (NotifierFactory) – Low
- No significant smell in the retry loop (must not invent one).

Bonus (found by agents and confirmed): `bus.publish(...)` sits inside the `try` around
`notifier.send`, so a throwing subscriber triggers a retry and a duplicate send. It is a bug,
reported separately from the refactoring.

## Expected behavior
- The report has an "Over-engineering to simplify" section with the 4 elements above.
- No proposal of **new** patterns.
- In Fix mode: a simplification plan in small steps (remove the proxy, inline the factory, remove
  the base class, replace the bus), **wait for approval**, green tests after every step, public
  API of `createNotificationService` unchanged (`notify`, `audit.all()`, `audit.count()`). Flags
  that removing exports (`EventBus`, `AuditLogProxy`, factories) may break external importers.

## Penalize
- Classifying `retryPolicies` as a smell or rewriting it as a class hierarchy.
- Calling `AuditLogProxy` a "sound" Proxy.
- Adding interfaces/factories "for future extensibility".
- Editing before approval ("simplify" is still a refactoring request).
