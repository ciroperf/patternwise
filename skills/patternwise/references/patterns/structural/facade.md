# Facade (Structural)

**Intent**: provide a simple interface to a complex subsystem (library, framework, set of
classes), exposing only what clients actually need.

## Problem it solves
- Business code is tangled with the initialization and call sequence of many subsystem objects
  (Shotgun Surgery whenever the subsystem changes; Message Chains across it).
- Layering: you want one entry point per subsystem.

## Roles
- **Facade**: knows the subsystem, orchestrates calls, offers task-level methods.
- **Additional Facades** (optional): split to avoid one facade becoming a God object.
- **Subsystem classes**: unaware of the facade.
- **Client**: uses the facade instead of the subsystem.

## Recognize it
- A class with few high-level methods (`convertVideo(file, format)`, `placeOrder(cart)`) each
  orchestrating several lower-level objects; application services in layered/hexagonal designs.

## Red flags
- Facade grows into a God object with dozens of unrelated methods → split by task/subsystem.
- Facade that forwards 1:1 to one class → Middle Man.
- Clients bypassing the facade anyway → it is not the real boundary.
- Business rules living in the facade instead of the domain (anemic domain).

## Don't use when
- The subsystem is already simple, or clients need its full flexibility.

## Idiomatic forms
- Module `__init__`/index exports, service classes, SDK "client" objects, application services.

## Path to it
Extract Method on the orchestration code in clients → Move Method into a new class (Extract Class)
→ Hide Delegate for message chains → clients call the facade.

## Trade-offs
+ Isolates clients from subsystem complexity and changes. − Risk of God object coupled to all
classes in the app.

## Related
Adapter wraps one object and changes its interface; Facade defines a new interface over many.
Mediator centralizes two-way communication between peers that know it; Facade's subsystem does not
know the facade. Often a single instance. Abstract Factory can hide subsystem creation.
