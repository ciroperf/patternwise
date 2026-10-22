# Factory Method (Creational)

**Intent**: define an interface for creating an object but let subclasses (or implementations)
decide which concrete class to instantiate, so the creator's logic works with any product.

## Problem it solves
- Core logic hard-codes `new ConcreteX()` and now a second product type must be supported; the
  logic around creation is the same.
- A framework/library must let users substitute their own component type.
- Creation of the same product family is spread through code with `if type == ...` choices.
- Expensive objects (connections, file handles) should be reused from a pool instead of rebuilt:
  a constructor must always return a new object, a factory method can return an existing one.

## Roles
- **Product**: interface common to all created objects.
- **Concrete Products**.
- **Creator**: declares `createProduct()` returning Product; contains business logic that uses it
  (the factory method is not the creator's main job).
- **Concrete Creators**: override `createProduct()`.

## Recognize it
- An overridable (abstract/virtual) method returning an interface type, called by other methods of
  the same class hierarchy.
- Framework hook methods like `createView()`, `newThread()`, `createConnection()` overridden by users.

## Red flags
- **Name only**: a static `XFactory.create(type)` with a switch → *simple factory* (fine if it is the
  single place mapping input → class; misleading if called "Factory Method").
- Factory method returning a concrete type → no substitution possible.
- Parallel hierarchy of creators that mirrors products 1:1 just to call constructors → consider
  passing a constructor/function instead.

## Don't use when
- Only one product type exists and no extension point is required: call the constructor.
- The variation is a data value, not a type: pass it as a parameter.

## Idiomatic forms
- Pass a factory function/lambda/class reference (`Callable[[], Product]`, `() => Product`,
  `Supplier<Product>`) instead of subclassing the creator.
- Map from key to constructor (`{"csv": CsvExporter, "json": JsonExporter}`) as a simple factory.
- DI containers often play this role; use them if the project does.

## Path to it
Replace Constructor with Factory Method → Extract Method (creation) → make it overridable in
the creator → Extract Interface for the product → subclasses override creation. Often follows
Replace Type Code with Subclasses.

## Trade-offs
+ Decouples creator logic from concrete products; Open/Closed for new products; single place for
creation. − More classes (subclass per product), especially if creators exist only to create.

## Related
Often evolves into Abstract Factory, Prototype or Builder. Abstract Factory is usually a set of
factory methods. Template Method frequently calls a factory method as one of its steps.
