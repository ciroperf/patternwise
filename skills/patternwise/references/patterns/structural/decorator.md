# Decorator (Structural)

**Intent**: attach extra behavior to an object dynamically by wrapping it in objects that share
its interface; wrappers can be stacked.

## Problem it solves
- Subclass explosion for combinations of optional features (`CompressedEncryptedStream`,
  `LoggingCachingRepository`).
- Need to add/remove behavior at runtime or per instance (logging, caching, retries, metrics,
  authorization, compression) without touching the core class.
- Cannot subclass (final class) or inheritance is a poor fit (Refused Bequest).

## Roles
- **Component** interface.
- **Concrete Component**: the core behavior.
- **Base Decorator** (optional): holds a Component and forwards everything.
- **Concrete Decorators**: add behavior before/after delegating.

## Recognize it
- A class implementing interface I that holds a field of type I received in the constructor and
  calls it in every method, adding something; stacked construction `new A(new B(new Core()))`.

## Red flags
- Wrapper that only forwards (no behavior) → Middle Man.
- Decorator whose behavior depends on its position in the stack (order-sensitive without docs).
- Decorator that sometimes skips delegation → actually Proxy or Chain of Responsibility; name
  accordingly.
- Clients checking the concrete type of the wrapped object → breaks transparency.

## Don't use when
- A single fixed combination is needed: compose directly in one class.

## Idiomatic forms
- Python function decorators / TS higher-order functions (for functions), HTTP middleware,
  stream wrappers (Java I/O), Kotlin `by` delegation, React HOCs.

## Path to it
Replace Inheritance with Delegation (for each feature subclass) → Extract Interface shared by core
and features → each feature becomes a wrapper → build combinations at the composition root.

## Trade-offs
+ Combine behaviors at runtime, SRP per concern, avoids subclass explosion.
− Many small objects; order matters; debugging layered stacks; removing a specific wrapper is hard.

## Related
Adapter changes the interface, Decorator keeps/extends it; Proxy manages lifecycle, Decorator is
composed by the client; Composite has many children; Chain of Responsibility can stop the flow;
Strategy changes the "guts", Decorator the "skin".
