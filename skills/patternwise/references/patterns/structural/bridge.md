# Bridge (Structural)

**Intent**: split a large class or hierarchy that varies along two independent dimensions into
two hierarchies — abstraction and implementation — connected by composition.

## Problem it solves
- Subclass explosion: `Shape × Color`, `Report × Exporter`, `Remote × Device`, where every new
  value of one dimension multiplies classes in the other (Parallel Inheritance Hierarchies).
- Need to switch the implementation at runtime, or support several platforms/backends behind the
  same high-level logic.

## Roles
- **Abstraction**: high-level control logic; holds a reference to an Implementation.
- **Refined Abstractions**: variants of the control logic.
- **Implementation** interface: primitive operations the abstraction relies on.
- **Concrete Implementations**: platform/backend specific.

## Recognize it
- Two hierarchies; one holds a field typed as the other's interface and delegates primitive
  operations to it; both sides have multiple subclasses.

## Red flags
- Only one implementation and no plan for another → over-engineered (one hierarchy is enough).
- Implementation interface mirroring the abstraction 1:1 → it is just delegation (Middle Man).
- Abstraction downcasting the implementation → broken separation.

## Don't use when
- Only one dimension varies (Strategy or plain subclassing is enough).

## Idiomatic forms
- Constructor-injected interface (DI) is the everyday Bridge; device drivers; renderer backends;
  storage abstraction over drivers.

## Path to it
Identify the two dimensions in class names (Parallel Inheritance / combinatorial subclasses) →
Extract Class for one dimension → Replace Inheritance with Delegation → Extract Interface for the
implementation side → collapse the multiplied subclasses.

## Trade-offs
+ Independent extension of both sides (OCP), platform independence, hides implementation details.
− More indirection; harder to read when the separation is not real.

## Related
Structure similar to Strategy/State (composition + delegation) but aims at whole-hierarchy
separation. Abstract Factory can create matching abstraction/implementation pairs. Adapter is for
after-the-fact compatibility, Bridge for up-front design.
