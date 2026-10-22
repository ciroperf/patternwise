# Visitor (Behavioral)

**Intent**: separate operations from the object structure they work on, so new operations can be
added without modifying the element classes.

## Problem it solves
- A stable set of element types (AST nodes, document elements, geometry shapes) and an
  ever-growing list of operations (export, render, validate, compute) that would otherwise bloat
  every element class or need `instanceof` chains.
- Auxiliary behaviors (export, reporting) clutter the primary classes; or a behavior makes sense
  only for some classes of the hierarchy (visitor implements only those, others are no-ops).

## Roles
- **Visitor** interface: one `visitX(x)` per concrete element type.
- **Concrete Visitors**: one per operation.
- **Element** interface: `accept(visitor)`.
- **Concrete Elements**: `accept` calls `visitor.visitX(this)` (double dispatch).
- **Client**: iterates the structure (often a Composite) and applies visitors.

## Recognize it
- `accept(Visitor)` methods; visitor interfaces with overloads per type; compiler/linters AST
  visitors.

## Red flags
- Element hierarchy changes often → every visitor must change (wrong axis; use polymorphism).
- Visitors needing private element internals → encapsulation broken by getters.
- "Visitor" doing `instanceof` instead of double dispatch → not the pattern.
- Single operation → over-engineering.

## Don't use when
- Element types change more often than operations; or the language has exhaustive pattern
  matching on closed types (use `match`/`switch` with sealed types instead).

## Idiomatic forms
- `functools.singledispatch`, pattern matching on sealed/ADT types, `std::visit` on variants,
  library-provided AST visitors/walkers.

## Path to it
Extract Method for each per-type branch of an operation → Move Method into a visitor class with
one method per element type → add `accept` to elements → replace type checks with double dispatch.

## Trade-offs
+ OCP for operations; operation logic cohesive in one class; can accumulate state while
traversing. − Adding element types touches all visitors; may need access to element internals.

## Related
Powerful Command over a structure. Often walks a Composite, sometimes with an Iterator.
