# Abstract Factory (Creational)

**Intent**: produce families of related objects that must be used together, without
specifying their concrete classes.

## Problem it solves
- Several product types must match each other (UI widgets per platform, DB driver + dialect +
  connection per vendor, storage + queue per cloud) and mixing them is a bug.
- Code is full of `if (platform == X) new XButton() ... if (platform == X) new XCheckbox()`.
- A class has accumulated several factory methods that blur its primary responsibility:
  extract them into a standalone factory (or a full Abstract Factory if families exist).

## Roles
- **Abstract Products**: one interface per product kind (Button, Checkbox).
- **Concrete Products**: per family (WinButton, MacButton).
- **Abstract Factory**: interface with one creation method per product kind.
- **Concrete Factories**: one per family; return products of that family.
- **Client**: receives a factory (chosen once, at startup/config) and uses only interfaces.

## Recognize it
- An interface with several `createX/createY` methods; multiple implementations each tied to one
  variant (vendor, platform, theme); the implementation is selected once and injected.

## Red flags
- **One family only** → over-engineering; use plain constructors or factory functions.
- Products from different families mixed through the same factory → broken invariant.
- Adding a product kind requires editing every factory: normal cost, but if new kinds are frequent
  and families rare, the pattern may be the wrong axis.

## Don't use when
- Families do not exist or never need to be consistent.
- The only variant need is tests: inject individual dependencies instead.

## Idiomatic forms
- A struct/object/record of factory functions; a module per family exporting the same functions;
  DI container profiles/modules per environment.

## Path to it
Collect scattered creation conditionals with Replace Constructor with Factory Method → group the
factory methods per family with Extract Class → Extract Interface across the family classes →
choose the concrete factory once at the composition root.

## Trade-offs
+ Guarantees product compatibility; isolates concrete classes; easy to swap whole families.
− Many interfaces/classes; adding a new product kind changes all factories.

## Related
Built from Factory Methods (sometimes Prototypes). Concrete factories are often single instances.
Can replace Facade's subsystem-creation logic. Pairs with Bridge (factory creates matching
abstraction/implementation pairs).
