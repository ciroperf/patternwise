# Template Method (Behavioral)

**Intent**: define the skeleton of an algorithm in a base class and let subclasses override
specific steps without changing the overall structure.

## Problem it solves
- Several classes implement the same algorithm with the same sequence of steps and duplicated
  code, differing in a few steps (data importers for CSV/XML/JSON; report generators; game AI turns).

## Roles
- **Abstract Class**: the template method (calls steps in order; ideally not overridable),
  abstract steps, optional hooks with default empty behavior.
- **Concrete Classes**: override steps/hooks only.

## Recognize it
- A non-overridden (final/sealed) method calling several abstract/protected methods; framework base
  classes with `onX`/`beforeX`/`afterX` hooks.

## Red flags
- Subclasses overriding the template method itself → skeleton not stable.
- Too many steps/hooks → hard to understand which to override (consider Strategy).
- Subclass that suppresses a default step by overriding with empty body (LSP issue, Refused Bequest).
- One subclass only → Collapse Hierarchy.

## Don't use when
- Variation is better expressed by passing functions; multiple dimensions vary (inheritance can
  express only one).

## Idiomatic forms
- Higher-order function receiving the varying steps; Go: function fields or small interfaces;
  framework lifecycle hooks.

## Path to it
Form Template Method: Extract Method for each step in sibling classes → unify names/signatures →
Pull Up Method for identical steps and the skeleton → abstract the differing steps.

## Trade-offs
+ Removes duplication; subclasses override only what varies. − Inheritance coupling; skeleton
constraints; LSP traps; harder to maintain with many steps.

## Related
Factory Method is a specialization (a step that creates). Strategy is the composition-based
alternative working at object level and runtime.
