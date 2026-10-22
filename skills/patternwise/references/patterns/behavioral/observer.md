# Observer (Behavioral)

**Intent**: define a subscription mechanism so that many objects get notified when something
happens to the object they observe, without the publisher depending on them.

## Problem it solves
- A class directly calls several unrelated modules after an event (`order.place()` calls email,
  analytics, inventory...), so every new reaction edits the publisher (Divergent Change).
- The set of interested parties changes at runtime.

## Roles
- **Publisher**: keeps subscribers, offers `subscribe/unsubscribe`, notifies on events.
- **Subscriber** interface: `update(event/context)`.
- **Concrete Subscribers**: react.
- **Client**: wires subscribers to publishers.

## Recognize it
- Listener lists, `addEventListener`, `on/emit`, signals/slots, domain events, reactive streams,
  property-change listeners.

## Red flags
- One publisher, one hard-wired subscriber → indirection only; call directly.
- Subscribers relying on notification order → hidden coupling.
- Missing unsubscribe → memory leaks (lapsed listener).
- Cascading notifications/cycles; synchronous heavy work in notify blocking the publisher.
- Events used to hide what is really a required step of a transaction (failure of a subscriber
  should abort but cannot).

## Don't use when
- Reactions are fixed, few, and part of the core use case; explicit calls are clearer.

## Idiomatic forms
- Framework event systems (DOM, Node EventEmitter, Django signals, Spring events, C# events),
  reactive libraries (RxJS, Flow), UI state frameworks.

## Path to it
Extract Interface for the reaction → Move Method of each reaction into its own subscriber →
publisher holds a list of subscribers and notifies → wire subscribers at startup
(Duplicate Observed Data for UI/domain sync).

## Trade-offs
+ OCP for new subscribers; runtime relationships. − Notification order unspecified; flow hard to
follow; leaks.

## Related
Mediator can be implemented with Observer; CoR/Command/Mediator are alternative connections.
