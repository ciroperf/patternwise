# Proxy (Structural)

**Intent**: provide a substitute with the same interface as a service object to control access to
it — doing something before/after forwarding, or deciding whether/when to forward.

## Problem it solves
- Expensive object that should be created lazily (virtual proxy).
- Access control (protection proxy), remote object (remote proxy/stub), result caching (caching
  proxy), request logging/auditing (logging proxy), resource cleanup when unused (smart reference).
- These concerns are mixed into business code or duplicated across callers.

## Roles
- **Service Interface**.
- **Service**: real business logic.
- **Proxy**: implements the same interface, holds/creates the service, adds control.
- **Client**: uses the interface, unaware of the proxy.

## Recognize it
- Same interface as the wrapped object; often the proxy creates/manages the service itself; ORM lazy
  loading, RPC stubs, generated dynamic proxies (Spring AOP, `java.lang.reflect.Proxy`, JS `Proxy`).

## Red flags
- Proxy that forwards everything without control → Middle Man.
- Proxy changing semantics (e.g. caching mutable results without invalidation) → stale data bugs.
- Proxy with a different interface → it is an Adapter.

## Don't use when
- The control logic is needed in one place only: keep it at the call site or in the service.

## Idiomatic forms
- Framework interceptors/AOP, ORM lazy relations, `functools.cache`, JS `Proxy`, gRPC stubs.

## Path to it
Extract Interface from the service → Extract Class for the cross-cutting control code → the new
class implements the interface and delegates → wire it at the composition root.

## Trade-offs
+ Controls the service transparently; manages lifecycle; OCP for new proxies.
− Adds latency/indirection; more classes; behavior hidden from readers.

## Related
Adapter: different interface. Decorator: same structure but composition decided by the client and
always delegating; Proxy usually manages the service lifecycle. Facade: new simplified interface.
