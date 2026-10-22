# Organizing Data

Replace raw data and type codes with meaningful types, and control how data is accessed.
Cure for Primitive Obsession, Data Class, Data Clumps and type-code Switch Statements.

Format: **When** · **Steps** · **Watch out** · **Treats**.

## Self Encapsulate Field
- **When**: you need a hook on field access (lazy init, validation, subclass override), or as
  a prelude to Move Field.
- **Steps**: add getter/setter; replace direct accesses (even inside the class) with them.
- **Watch out**: do not do it reflexively; language properties may already give you this.

## Replace Data Value with Object
- **When**: a primitive field gains behavior/validation (phone, money, email, date range).
- **Steps**: create a class (prefer immutable value object) holding the value; change the
  field type; update getters/setters to wrap/unwrap; move related behavior in.
- **Treats**: Primitive Obsession, Duplicate Code (repeated validation), Data Clumps.

## Change Value to Reference
- **When**: many identical value copies must become one shared entity (updates must be seen
  everywhere — a Customer, not a string).
- **Steps**: Replace Constructor with Factory Method; decide where instances live (repository/
  registry/identity map); make the factory return the shared instance.
- **Watch out**: identity vs equality, lifecycle and concurrency of the shared object.

## Change Reference to Value
- **When**: a reference object is small, rarely changes, and managing identity is not worth it.
- **Steps**: make it immutable (remove setters); implement value equality and hashing; drop the
  registry/factory if no longer needed.
- **Leads to**: Flyweight (sharing immutable values).

## Replace Array with Object
- **When**: an array/tuple holds heterogeneous fields by position (`row[0]` = name, `row[1]` = score).
- **Steps**: create a class with a field per element; migrate accesses one index at a time.
- **Treats**: Primitive Obsession.

## Duplicate Observed Data
- **When**: domain data/logic lives in UI/controller classes.
- **Steps**: create a domain class with the data; keep UI and domain in sync via observation
  (events/bindings/framework state); move logic to the domain class.
- **Leads to**: Observer; MVC/MVVM separation. Usually the framework provides the mechanism.
- **Treats**: Large Class (UI), Divergent Change.

## Change Unidirectional Association to Bidirectional
- **When**: both classes really need to navigate to each other.
- **Steps**: add the back reference; choose one side to control the association; update both
  sides through that controller's methods.
- **Watch out**: creates coupling and cycles — only when necessary.

## Change Bidirectional Association to Unidirectional
- **When**: one direction is not used, or can be derived/passed in.
- **Steps**: replace uses of the unwanted side with a parameter or a query; remove the field and
  the sync code.
- **Treats**: Inappropriate Intimacy; simplifies GC and testing.

## Replace Magic Number with Symbolic Constant
- **When**: a literal with meaning (`9.81`, `0.22` VAT, `86400`) appears in code.
- **Steps**: declare a well-named constant; replace each occurrence *that has the same meaning*.
- **Watch out**: same number, different meaning → different constants. Type codes deserve an
  enum/class (see below), not a constant.

## Encapsulate Field
- **When**: a public field.
- **Steps**: make it private; add accessors (or properties); update clients.

## Encapsulate Collection
- **When**: a getter returns a mutable internal collection, a setter replaces it wholesale.
- **Steps**: add `add/remove` methods; make the getter return a read-only view or copy;
  replace setters with initialization + add/remove; update clients.
- **Treats**: Data Class, Inappropriate Intimacy. **Leads to**: Iterator.

## Replace Type Code with Class
- **When**: a type code (int/string constants) does not affect behavior (no switch on it).
- **Steps**: create a class/enum with the allowed values; change field and parameters to the
  new type; remove the old constants.
- **Treats**: Primitive Obsession (type safety).

## Replace Type Code with Subclasses
- **When**: the type code drives behavior via conditionals **and** never changes after
  creation **and** the class is not already subclassed for another reason.
- **Steps**: Self Encapsulate the type field; create a factory method choosing the subclass;
  create one subclass per code value overriding the type getter; move behavior per type with
  Replace Conditional with Polymorphism; remove the field.
- **Leads to**: Factory Method, polymorphic dispatch.
- **Treats**: Switch Statements.

## Replace Type Code with State/Strategy
- **When**: the type code drives behavior **and** can change at runtime, or the class already has
  subclasses.
- **Steps**: Self Encapsulate the type field; create an abstract state/strategy type and one
  implementation per code; host class holds a reference to the current state/strategy;
  setter swaps the object; move per-type behavior with Replace Conditional with Polymorphism.
- **Choose**: State when the object's lifecycle status changes and states trigger transitions;
  Strategy when an algorithm is chosen by the client/config.
- **Treats**: Switch Statements, Large Class.

## Replace Subclass with Fields
- **When**: subclasses differ only in constant-returning methods.
- **Steps**: add fields to the parent for those constants; factory method sets them; remove the
  subclass overrides and then the subclasses.
- **Treats**: Lazy Class, Speculative Generality, Parallel Inheritance Hierarchies.
