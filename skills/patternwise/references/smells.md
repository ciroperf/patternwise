# Code smells

A smell is a surface symptom suggesting a deeper design problem. It is evidence, not a
verdict: always check the cause and the cost before recommending a change.

Each entry: **Signs** (what to look for) · **Why it happens** · **Treatment** (techniques,
see `refactorings/`) · **May lead to** (patterns, see `patterns/`) · **Leave it when**.

Families (refactoring.guru taxonomy): Bloaters, Object-Orientation Abusers, Change
Preventers, Dispensables, Couplers, plus Other.

---

## 1. Bloaters

Code that has grown so large it is hard to hold in your head. Usually accumulates slowly.

### Long Method
- **Signs**: a function doing several things; needs scrolling; comment headers splitting it
  into sections; deep nesting; many local variables. Rough threshold: > ~10–20 lines of
  logic deserves a question (adapt to language and team norms).
- **Why**: adding two lines to an existing function always feels cheaper than creating one.
- **Treatment**: Extract Method (a commented block is a natural candidate; the comment becomes
  the name). Many temps → Replace Temp with Query, Introduce Parameter Object, Preserve
  Whole Object. Temps too entangled → Replace Method with Method Object. Conditionals →
  Decompose Conditional. Loops → Extract Method on the loop body.
- **May lead to**: Template Method (several long methods with same skeleton), Command
  (Method Object that gets queued/undone), Strategy.
- **Leave it when**: it is a linear, flat sequence (e.g. a config table, a test arrange
  block) where splitting would only scatter reading.

### Large Class (God Object)
- **Signs**: many fields/methods/lines; methods that use disjoint subsets of fields; name
  ending in Manager/Service/Utils/Helper holding unrelated duties; changes for many reasons.
- **Why**: classes start small, every feature lands in the "obvious" place.
- **Treatment**: Extract Class (cohesive field+method clusters), Extract Subclass (behavior
  used only in some cases), Extract Interface (list of operations clients use), Duplicate
  Observed Data (domain logic mixed into UI).
- **May lead to**: Facade (if the class is the entry point for a subsystem, keep a thin
  facade over extracted parts), Strategy/State, Mediator (if it coordinates many objects).
- **Leave it when**: it is a cohesive aggregate (one responsibility, many small methods).

### Primitive Obsession
- **Signs**: strings/ints for domain concepts (money, email, currency, ranges, phone);
  constants for type codes (`ROLE_ADMIN = 1`); string keys into arrays as fields; validation
  of the same primitive repeated in many places.
- **Why**: a primitive field is quicker than a class; then it multiplies.
- **Treatment**: Replace Data Value with Object; Introduce Parameter Object / Preserve Whole
  Object for groups; type codes → Replace Type Code with Class / Subclasses / State/Strategy;
  arrays-as-records → Replace Array with Object.
- **May lead to**: Value Object (not GoF, but the main target), State, Strategy, Flyweight
  (many shared immutable values).
- **Leave it when**: the value has no rules or behavior and appears in one place.

### Long Parameter List
- **Signs**: > 3–4 parameters; boolean flag parameters; callers computing values the callee
  could obtain itself.
- **Why**: merging algorithms into one function; or reducing coupling by passing everything in.
- **Treatment**: Replace Parameter with Method Call; Preserve Whole Object; Introduce
  Parameter Object; flags → Replace Parameter with Explicit Methods.
- **May lead to**: Builder (complex construction), Command (parameters packaged as an object).
- **Leave it when**: removing parameters would create an unwanted dependency between classes.

### Data Clumps
- **Signs**: the same group of variables travels together (start/end dates, host/port/user,
  x/y/z) through fields and signatures. Test: delete one; do the others still make sense?
- **Treatment**: Extract Class for fields; Introduce Parameter Object / Preserve Whole Object
  for signatures; then Move Method behavior into the new class.
- **May lead to**: Value Object.
- **Leave it when**: grouping would couple two classes that should stay independent.

---

## 2. Object-Orientation Abusers

Incomplete or incorrect use of OO mechanisms.

### Switch Statements (type-based conditionals)
- **Signs**: `switch`/`if-elif`/`match` on a type code, enum or `instanceof`, **repeated** in
  several places; adding a variant means editing all of them.
- **Treatment**: Extract Method + Move Method to put the switch where the data is; then
  Replace Type Code with Subclasses or Replace Type Code with State/Strategy; then Replace
  Conditional with Polymorphism. Parameter-driven branches → Replace Parameter with Explicit
  Methods. A `null` branch → Introduce Null Object.
- **May lead to**: Strategy, State, Command, Visitor (if variants are stable but operations
  grow), Factory Method / map of constructors to pick the variant once.
- **Leave it when**: a single switch, simple actions, in one place (e.g. the one factory
  that maps input to an object); or the language favors exhaustive pattern matching over
  closed sum types (Rust, Kotlin sealed, TS discriminated unions, Scala, F#) — there,
  exhaustive matching is idiomatic and safe.

### Temporary Field
- **Signs**: fields set and used only in some scenarios, empty/null otherwise; often holding
  inputs of a complex algorithm to avoid long parameter lists.
- **Treatment**: Extract Class (or Replace Method with Method Object) for the fields and the
  code that uses them; Introduce Null Object for the "is it set?" checks.
- **May lead to**: Command (Method Object), Null Object.

### Refused Bequest
- **Signs**: a subclass uses few inherited members, overrides some to throw/do nothing; the
  "is-a" relation is false (inheritance used only for code reuse).
- **Treatment**: if inheritance is wrong: Replace Inheritance with Delegation. If it is right
  but the parent is too broad: Extract Superclass with only what is shared (or Push Down
  Method/Field).
- **May lead to**: composition-based designs (Decorator, Strategy, Bridge). See Liskov in
  `principles.md`.

### Alternative Classes with Different Interfaces
- **Signs**: two classes do the same job with different method names/signatures.
- **Treatment**: Rename Method, Move Method, Add/Parameterize; if only part is duplicated,
  Extract Superclass; when one is redundant, delete it.
- **May lead to**: Adapter (when one side is third-party and cannot change), Strategy.
- **Leave it when**: the classes live in different libraries, each with its own version;
  merging would cost more than it saves.

---

## 3. Change Preventers

One change forces edits in many places.

### Divergent Change
- **Signs**: one class edited for many unrelated reasons ("for a new product type I change
  methods A,B,C; for a new payment I change D,E,F").
- **Treatment**: Extract Class per reason to change; Extract Superclass/Subclass when the
  variants share behavior.
- **May lead to**: SRP-aligned modules; Strategy, Bridge (two independent dimensions).

### Shotgun Surgery
- **Signs**: one conceptual change touches many classes in small ways (opposite of
  Divergent Change). Check git history: files that always change together.
- **Treatment**: Move Method / Move Field to gather the behavior in one class (create one if
  needed); Inline Class to merge scattered fragments.
- **May lead to**: Facade, Mediator, Observer (central notification instead of scattered calls).

### Parallel Inheritance Hierarchies
- **Signs**: adding a subclass to one hierarchy requires adding one to another (prefixes match:
  `XmlReport`/`XmlFormatter`). In dynamic languages the hierarchies are often implicit
  (duck-typed classes with no common base): look for 1:1 pairs where each class hardwires
  its partner (`self.formatter = HtmlFormatter()`).
- **Treatment**: make instances of one hierarchy refer to the other, then Move Method/Field
  to eliminate the second hierarchy.
- **May lead to**: Bridge (if both dimensions are genuinely independent), Abstract Factory
  (if the parallel families must be used together).
- **Leave it when**: merging makes the code worse; then at least keep the coupling explicit.

---

## 4. Dispensables

Something pointless whose removal would make code cleaner.

### Comments (explaining what, not why)
- **Signs**: comments that narrate what code does, or apologise for confusing code.
- **Treatment**: Extract Variable for complex expressions; Extract Method with a name taken
  from the comment; Rename Method; Introduce Assertion for stated preconditions.
- **Leave it when**: the comment explains *why* (constraints, workarounds, rationale), explains
  a complex algorithm after simplification attempts failed, or documents a public API.

### Duplicate Code
- **Signs**: identical or near-identical fragments; same algorithm in different forms.
- **Treatment**: same class → Extract Method; sibling subclasses → Extract Method + Pull Up
  Method/Field (Pull Up Constructor Body); similar but not identical → Form Template Method;
  same goal different algorithm → Substitute Algorithm; unrelated classes → Extract
  Superclass or Extract Class; many conditionals with same result → Consolidate Conditional
  Expression; same code in all branches → Consolidate Duplicate Conditional Fragments.
- **May lead to**: Template Method, Strategy.
- **Leave it when**: the duplicates are coincidental and will evolve differently (merging
  would couple unrelated concepts). "Rule of three" is a good guide.

### Lazy Class
- **Signs**: a class that does too little to justify itself (often after refactoring, or
  created for future needs).
- **Treatment**: Inline Class; Collapse Hierarchy for near-empty subclasses.
- **Leave it when**: it is a deliberate seam (a port in hexagonal architecture, a test
  double target that is actually used), or it marks an agreed, imminent extension — balance
  clarity against simplicity.

### Data Class
- **Signs**: only fields + getters/setters; all the behavior on that data lives elsewhere.
- **Treatment**: Encapsulate Field, Encapsulate Collection, Remove Setting Method; then Move
  Method / Extract Method to bring the behavior that uses the data into the class; Hide Method
  for accessors no longer needed.
- **Leave it when**: it is a DTO/record at a boundary (API payloads, ORM rows, messages) or
  the language/style is data-oriented (records + functions). Check the project's convention.

### Dead Code
- **Signs**: unused variables, parameters, fields, methods, classes, unreachable branches.
- **Treatment**: delete it (IDE/LSP "find references", compiler warnings, coverage). Remove
  Parameter; Inline Class / Collapse Hierarchy for unused hierarchy parts.
- **Caution**: check reflection, dependency injection, serialization, public APIs, plugin
  entry points and templates before deleting.

### Speculative Generality
- **Signs**: abstract classes, hooks, parameters, interfaces created "in case"; a single
  implementation behind an abstraction with no test or runtime need.
- **Treatment**: Collapse Hierarchy, Inline Class, Inline Method, Remove Parameter.
- **Leave it when**: it is a framework/library's public extension point used by clients you
  cannot see. Before deleting, check unit tests: they may legitimately use it as a seam.
- This is the main **over-engineering** smell: report it.

---

## 5. Couplers

Excessive coupling between classes, or delegation pushed too far.

### Feature Envy
- **Signs**: a method uses another object's data more than its own (many getters on another
  object).
- **Treatment**: Move Method; if only part of it envies, Extract Method then Move Method. If
  it envies several classes, move it next to the data it uses most.
- **Leave it when**: separation is deliberate (Strategy/Visitor keep behavior apart from data
  so it can vary independently; persistence mappers).

### Inappropriate Intimacy
- **Signs**: classes using each other's private/internal fields and methods; bidirectional
  dependencies; subclass reaching into parent internals.
- **Treatment**: Move Method/Field (if the first class really does not need those parts);
  Extract Class + Hide Delegate to make the relationship explicit; Change Bidirectional
  Association to Unidirectional for mutual dependencies; for subclass↔parent intimacy,
  Replace Delegation with Inheritance (only if the relation is genuinely is-a).
- **May lead to**: Mediator, Facade.

### Message Chains
- **Signs**: `a.getB().getC().getD().do()` — client depends on the navigation structure.
- **Treatment**: Hide Delegate; or Extract Method on the code using the final object and Move
  Method it to the start of the chain.
- **Leave it when**: fluent/builder APIs or immutable data navigation (that is not a chain of
  responsibilities, just syntax). Beware of creating Middle Man by overdoing Hide Delegate.

### Middle Man
- **Signs**: a class whose methods mostly delegate to another class.
- **Treatment**: Remove Middle Man; Inline Method for the few that add nothing.
- **Leave it when**: it is a deliberate Proxy, Decorator, Adapter or Facade that adds or hides
  something meaningful, or breaks a dependency between layers.

---

## 6. Other

### Incomplete Library Class
- **Signs**: a library lacks a method you need and you cannot modify it; helper code around it
  repeated across the codebase.
- **Treatment**: Introduce Foreign Method (one or two methods, in the client); Introduce Local
  Extension (subclass or wrapper with many additions). Use language features where they exist
  (extension functions, categories, traits).
- **May lead to**: Adapter, Decorator.
- **Leave it when**: the library changes often; every extension becomes extra work to keep
  in sync.

---

## Common anti-patterns related to patterns (report as smells)

- **Singleton as global mutable state**: hidden dependencies, test interference. Treat:
  pass the instance explicitly / via DI; keep a single instance at composition root.
- **Anemic "Manager/Service" + Data Classes**: procedural code dressed as OO. Treat: Move
  Method behavior next to data (unless the project deliberately uses a functional/DTO style).
- **Interface for every class**: Speculative Generality unless there is a second
  implementation, a test double, or a module boundary that needs it.
- **Pattern stacking**: Factory creating a Builder producing a Strategy wrapped by a Proxy
  for one use case. Treat: Inline Class / Collapse Hierarchy down to what varies.
- **Event soup**: Observer/event bus used for direct calls between two components, making
  control flow invisible. Treat: replace with direct calls when there is one listener and no
  need for decoupling.
