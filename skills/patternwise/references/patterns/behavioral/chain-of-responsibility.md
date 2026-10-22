# Chain of Responsibility (Behavioral)

**Intent**: pass a request along a chain of handlers; each handler decides to process it, pass it
on, or both — so the sender does not know which handler will act.

## Problem it solves
- A growing sequence of checks/processing steps (auth → validation → rate limit → cache → handler)
  hard-coded in one method, with steps reused or reordered in different flows.
- Several candidate handlers whose selection must be decided at runtime.

## Roles
- **Handler** interface: `handle(request)`; optionally `setNext(handler)`.
- **Base Handler** (optional): stores next and forwards by default.
- **Concrete Handlers**: process and/or forward.
- **Client**: builds the chain (or receives it) and sends requests to its head.

## Recognize it
- Middleware pipelines (`next()`), servlet filters, event bubbling in UI trees, exception handler
  lists, a list of handlers iterated until one returns "handled".

## Red flags
- Chain order is significant but implicit/undocumented → fragile.
- Requests that fall off the end silently when they should fail.
- Handlers that know about specific other handlers → coupling defeats the purpose.
- A fixed 2-step sequence wrapped in a chain → over-engineering.

## Don't use when
- Steps are few, fixed and always all executed: a plain sequence of calls is clearer.

## Idiomatic forms
- Framework middleware (Express, ASP.NET, Django, Go `http.Handler` wrappers), a list of functions
  `[(req) -> Response | None]` iterated in order.

## Path to it
Decompose Conditional → Extract Method per check → Extract Class per handler with a common
interface → the original method builds/iterates the chain.

## Trade-offs
+ Control order of handling; SRP per handler; OCP for new handlers. − Some requests may go
unhandled; debugging flow across many handlers.

## Related
Often used with Composite (requests travel up to parents). Command objects can be the requests.
Decorator has the same structure but cannot stop the flow. Mediator/Observer are other ways to
connect senders and receivers.
