# Flyweight (Structural)

**Intent**: fit more objects in memory by sharing the common, immutable part of their state
(intrinsic) and passing the varying part (extrinsic) from outside.

## Problem it solves
- A huge number of similar objects (particles, glyphs, map tiles, tree sprites) exhausts memory, and
  much of each object's state is duplicated and immutable.
- Only relevant when the memory problem is **measured**.

## Roles
- **Flyweight**: immutable intrinsic state + methods that receive extrinsic state as parameters.
- **Context**: per-object extrinsic state + reference to a flyweight.
- **Flyweight Factory**: cache returning existing flyweights for the same intrinsic state.
- **Client**: computes/stores extrinsic state.

## Recognize it
- Caches/pools keyed by value returning shared immutable instances; interning (`String.intern`,
  `Integer.valueOf` caches, symbol tables); "type" objects shared by many instances.

## Red flags
- Shared flyweights that are mutable → cross-object corruption (High).
- Applied without memory pressure → complexity for nothing.
- Factory cache that never evicts in a long-running process → leak.

## Don't use when
- Object counts are modest; memory is not a measured constraint.

## Idiomatic forms
- Interning, `functools.lru_cache` on constructors of immutable values, enum instances, ECS-style
  data separation (arrays of components).

## Path to it
Split intrinsic vs extrinsic state (Extract Class for intrinsic) → Change Reference to Value
(immutable) → Replace Constructor with Factory Method returning cached instances → move extrinsic
state to contexts and pass it as parameters.

## Trade-offs
+ Large memory savings. − CPU spent recomputing/passing extrinsic state; more complex code.

## Related
Composite leaves can be flyweights; differs from Singleton (many immutable shared instances vs one
mutable instance). State/Strategy objects without fields can be shared as flyweights.
