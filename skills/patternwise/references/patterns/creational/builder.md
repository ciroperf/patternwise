# Builder (Creational)

**Intent**: construct a complex object step by step, allowing different representations
from the same construction process and avoiding monster constructors.

## Problem it solves
- Telescoping constructors / constructors with many optional parameters and `null` placeholders.
- Construction requires ordered steps, validation of the combination, or produces an immutable
  object after configuration.
- The same construction steps must yield different products (e.g. a document as HTML or PDF).

## Roles
- **Builder** interface: step methods (`setX`, `addPart`, `withY`).
- **Concrete Builders**: implement steps and expose `build()/getResult()`.
- **Director** (optional): encodes a reusable order of steps.
- **Product**: the result; different builders may produce unrelated product types.

## Recognize it
- Fluent chain `X.builder().a(..).b(..).build()`; separate mutable builder producing an immutable
  object; validation in `build()`; director-like functions calling steps in order.

## Red flags
- Builder for 2–3 required fields → noise; use a constructor or named/default arguments.
- `build()` returns a half-initialized object (no validation) → false safety.
- Builder exposing setters on the product itself (product mutable after build) → not isolated.

## Don't use when
- The language has named/default arguments and the object is simple (Python, Kotlin, C#, TS object
  literals). Use those or a dataclass/record.

## Idiomatic forms
- Go functional options (`New(opts ...Option)`), Kotlin DSL builders / `apply {}`, Rust builder
  structs (very idiomatic), Lombok `@Builder`, test data builders in test code.

## Path to it
Introduce Parameter Object for the many parameters → Replace Constructor with Factory Method /
Extract Class into a builder → move validation into `build()` → Remove Setting Method on the product.

## Trade-offs
+ Readable construction; immutable products; reuse of construction sequences.
− Extra class per product; duplication of fields between builder and product.

## Related
Composite trees are often built with a Builder. Abstract Factory returns products immediately;
Builder assembles them over several steps. Can be combined with Bridge (director = abstraction).
