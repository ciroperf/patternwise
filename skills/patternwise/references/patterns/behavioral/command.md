# Command (Behavioral)

**Intent**: turn a request into a standalone object containing everything needed to perform it,
so requests can be passed around, queued, scheduled, logged, retried or undone.

## Problem it solves
- The same action triggered from several UI elements (button, menu, shortcut) duplicates the call
  to business logic, or UI classes contain business logic.
- Operations must be undone/redone, queued, delayed, executed remotely, retried, or recorded
  (audit, macro, transactional log).

## Roles
- **Command** interface: `execute()` (optional `undo()`).
- **Concrete Commands**: hold the receiver and the parameters; delegate the real work to it.
- **Receiver**: business object that does the work.
- **Invoker/Sender**: triggers commands, may store history/queue.
- **Client**: creates and configures commands.

## Recognize it
- Objects with a single `execute/run/call` method plus captured params; history stacks for undo;
  job/task queues with serialized task objects.

## Red flags
- "Command" objects that are pure data dispatched by a big switch in a handler → message/DTO, not
  Command (may be a fine CQRS design; label it correctly).
- Commands containing the entire business logic instead of delegating to receivers → logic
  scattered in commands.
- `undo()` that does not fully restore state (missing Memento/snapshot).

## Don't use when
- One call site, no undo/queue/log requirement: call the method.

## Idiomatic forms
- Closures/lambdas (`Runnable`, `() => void`, Python callables), `functools.partial`; job
  frameworks (Celery tasks, Sidekiq jobs) for queued commands.

## Path to it
Replace Method with Method Object (operation → object) → Extract Interface (`execute`) → move
callers (UI) to create and invoke commands → add history/undo if required.

## Trade-offs
+ Decouples invokers from receivers; undo/redo; deferred/queued execution; compose macros.
− An extra layer per action.

## Related
CoR handlers can be commands. Memento supports undo. Strategy describes *how* to do one thing;
Command *what* to do. Prototype can copy commands into history. Visitor ≈ a powerful command over
an object structure.
