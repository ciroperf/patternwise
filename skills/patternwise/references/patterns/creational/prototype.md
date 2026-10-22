# Prototype (Creational)

**Intent**: create new objects by copying an existing, configured instance, without depending
on its concrete class.

## Problem it solves
- Copying objects from outside requires knowing their concrete class and accessing private fields.
- Many variants differ only in configuration; creating subclasses per configuration is wasteful.
- Initialization is expensive and a configured template can be copied instead.

## Roles
- **Prototype** interface with `clone()`.
- **Concrete Prototypes** implement copying (deep vs shallow decided per field).
- **Registry** (optional): named pre-configured prototypes.

## Recognize it
- `clone()/copy()/duplicate()` implemented by the objects themselves; copy constructors used
  polymorphically; registries of templates.

## Red flags
- Shallow copy where nested mutable state is shared unintentionally (bug risk: High).
- Clone that ignores subclass fields; cyclic references not handled.
- `clone()` implemented but never used polymorphically → just a copy helper.

## Don't use when
- Objects are immutable (share them instead) or trivially constructible.

## Idiomatic forms
- Java `Cloneable` is discouraged; prefer copy constructors/`copy()` methods. Kotlin `data class
  copy()`, Python `copy.copy/deepcopy` or `dataclasses.replace`, Rust `Clone`, JS
  `structuredClone`/spread (shallow!).

## Path to it
Extract Method for the copying logic → move it into the class (Move Method) → Extract Interface
`Prototype` if clients copy polymorphically.

## Trade-offs
+ Copy without coupling to concrete classes; fewer configuration subclasses.
− Deep copy of complex graphs (cycles, external resources) is tricky.

## Related
Alternative to Factory Method subclasses; Abstract Factory can use prototypes. Useful with
Composite/Decorator to duplicate structures; Memento can sometimes be a clone.
