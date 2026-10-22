# Design principles (for justifying recommendations)

Use these to explain *why* a finding matters. Quote the principle only when it clarifies the
concrete problem; never as a substitute for evidence.

## Qualities we are optimizing for
- **Easy to change**: a typical change touches few places, all of them obvious.
- **Easy to understand**: names and structure reveal intent; no need to read implementations.
- **Safe to change**: behavior is pinned by tests; dependencies are explicit.
- **Reuse is a side effect, not a goal**: reuse via abstraction costs indirection; only pay
  when there are real reusers.

## OOP mechanics recap
- **Abstraction**: model only what the context needs.
- **Encapsulation**: hide state and internals behind behavior; clients use an interface.
- **Inheritance**: reuse + subtype. Strong coupling: subclass depends on parent internals
  and must honor its contract.
- **Polymorphism**: clients call through an abstract type, the concrete behavior is chosen at
  runtime; this is what replaces type switches.
- **Relations (weakest → strongest coupling)**: dependency (uses temporarily) < association
  (holds a reference) < aggregation (has-a, independent lifetime) < composition (owns parts'
  lifetime) < implementation (of an interface) < inheritance (of an implementation).

## Core design principles
- **Encapsulate what varies**: find the part that changes (a rule, a format, a provider) and
  isolate it behind a stable boundary (method → class → module). Most patterns are a form of
  this. Corollary: if nothing varies, do not encapsulate "variation".
- **Program to an interface, not an implementation**: depend on what you need (a capability),
  not on a concrete class. Apply when there are, or will soon be, several implementations,
  or to break a dependency on infrastructure. A single implementation does not need an interface
  unless a test seam or module boundary needs it.
- **Favor composition over inheritance**: inheritance cannot hide parent details, forces the
  full parent interface on children, couples to parent changes, and explodes combinatorially
  with several dimensions (`Truck×Electric×Autopilot`). Composition allows runtime swapping
  and independent dimensions (Strategy, Bridge, Decorator).

## SOLID
- **S – Single Responsibility**: a class/module should have one reason to change (one actor or
  concern). Detected by Divergent Change and Large Class. Over-applying it produces Lazy
  Classes and Shotgun Surgery; balance with cohesion.
- **O – Open/Closed**: extend behavior by adding code, not editing stable code. Valid where
  variation actually happens (type switches that grow). Do not pre-open everything.
- **L – Liskov Substitution**: subtypes must be usable wherever the parent is expected:
  parameters not narrower, return types not wider, no new exceptions, preconditions not
  stronger, postconditions not weaker, invariants kept, no writing to parent private state.
  Violations show up as `instanceof` checks and Refused Bequest.
- **I – Interface Segregation**: clients should not depend on methods they do not use; split
  fat interfaces (Extract Interface). Do not split into one-method interfaces with no client
  need.
- **D – Dependency Inversion**: high-level policy should not depend on low-level details; both
  depend on an abstraction owned by the high-level side (e.g. a repository interface in the
  domain, implemented in infrastructure).

## Simplicity guards
- **YAGNI**: no abstraction for a variation that does not exist now or in an agreed near-term
  plan. Write the simple version; refactor to the pattern when the second case arrives.
- **KISS**: prefer the construct a newcomer reads fastest. A function beats a class hierarchy
  when it does the same job.
- **Rule of three**: tolerate duplication twice; abstract the third time, when the shape of
  the variation is known.
- **Locality**: code that changes together should live together.
- **Indirection has a cost**: every layer must hide or decide something.

## Signals of over-engineering (report as findings)
- Interfaces/abstract classes with one implementation and no test double or boundary need.
- Factories/builders/providers that always return the same type.
- Strategy/State/Visitor/Command hierarchies with one or two trivial members.
- Configurable behavior that is never configured differently.
- Generic type parameters used with a single type.
- Event buses or observers with one publisher and one subscriber that could call directly.
- Layers that only forward (Middle Man), "manager of managers".
- Patterns introduced in advance of a requirement ("we might support other databases").

## Coupling and cohesion quick checks
- Afferent/efferent coupling: who depends on this, what does it depend on. Many dependents +
  frequent change = high risk.
- Cohesion: do methods use the same fields? Disjoint clusters → Extract Class.
- Dependency cycles between modules are a High finding when they block independent change.
