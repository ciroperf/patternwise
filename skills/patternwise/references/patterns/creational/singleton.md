# Singleton (Creational)

**Intent**: ensure a class has exactly one instance and provide a global access point to it.

## Problem it solves (rarely, legitimately)
- A resource that truly must be unique per process (hardware handle, process-wide registry) and
  must be shared.
Note: it solves two problems at once (uniqueness + global access), which violates SRP and is
the source of most misuse.

## Roles
- **Singleton**: private constructor, static instance field, static `getInstance()`, lazy or eager
  initialization, thread-safety if concurrent.

## Recognize it
- `getInstance()`/`instance`/`shared`/`default`; static holder; module-level object used everywhere;
  framework-scoped singletons (DI singleton scope — that is lifecycle management, not the pattern).

## Red flags (misapplied — common)
- Holds **mutable global state** read/written from many places → hidden coupling, order-dependent
  bugs, tests interfering with each other. Severity often High.
- Used as a convenient way to avoid passing dependencies (service locator in disguise).
- Not thread-safe lazy initialization in concurrent code.
- Multiple "singletons" depending on each other's initialization order.
- Tests needing `resetInstance()` hacks.

## Don't use when
- You just need one instance: create one at the composition root and pass it (DI). Uniqueness is a
  wiring decision, not a class property.

## Idiomatic forms
- Python/JS/Go module-level instance; Kotlin `object`; DI container singleton scope; Go
  `sync.Once`; Java enum singleton; Rust `OnceLock`/`LazyLock` (still global state!).

## Path away from it (usual recommendation)
Introduce Parameter / constructor injection of the instance in callers (start from leaves) → create
the single instance at the composition root → reduce `getInstance()` calls to zero → make the
constructor normal.

## Trade-offs
+ Guaranteed single instance, lazy initialization. − Global state, hidden dependencies, hard
testing, concurrency hazards, violates SRP.

## Related
Facade and Abstract Factory objects are often single instances — fine if passed explicitly.
Flyweight differs: many shared immutable instances vs one mutable instance.
