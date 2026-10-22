# Adapter (Structural)

**Intent**: let a client work with a class whose interface is incompatible, by wrapping it in an
object that translates calls (and data formats).

## Problem it solves
- A third-party/legacy component does what you need but with a different interface or data format
  (XML vs JSON, different units, callback vs promise), and you cannot or should not change it.
- Several providers with different APIs must be used through one interface (payment gateways, SMS).
- Several existing subclasses lack the same functionality that cannot go into their superclass:
  wrap them in one adapter instead of duplicating the feature in new child classes.

## Roles
- **Client** and **Client Interface** (owned by the client side).
- **Service/Adaptee**: the incompatible class.
- **Adapter**: implements the client interface, holds the adaptee, converts requests/results.
- (Class adapter variant: inherits both — only with multiple inheritance.)

## Recognize it
- A class implementing your interface whose methods mostly translate parameters and call a
  differently-shaped object; anti-corruption layers; "gateway"/"client" wrappers around SDKs.

## Red flags
- Adapter for an interface you own and could just change → Middle Man.
- Adapter leaking adaptee types in its interface → coupling not removed.
- Business logic inside the adapter (it should translate, not decide).
- 1:1 renaming wrapper around your own class → unnecessary.

## Don't use when
- You control both sides: change one interface (Rename Method / Move Method).

## Idiomatic forms
- A function converting callbacks to promises; extension functions; Go small interface satisfied
  by a thin struct; TS mapping functions between DTO shapes.

## Path to it
Extract Interface (from the client's needs) → Introduce Local Extension (wrapper) around the
adaptee → Move Method the conversion code from callers into the wrapper → callers depend on the
interface.

## Trade-offs
+ Isolates third-party APIs (SRP), swap providers (OCP). − Extra layer; keep it thin.

## Related
Bridge is designed up-front; Adapter retrofits. Decorator keeps the interface and adds behavior;
Proxy keeps the interface and controls access; Facade defines a new interface over many objects.
