# Moving Features between Objects

Put each responsibility where its data and its reason-to-change live. These are the main
cure for Couplers and Change Preventers. Medium risk: they cross class/file boundaries.

Format: **When** · **Steps** · **Watch out** · **Treats**.

## Move Method
- **When**: a method uses another class's data more than its own.
- **Steps**: check what the method uses in its current class (fields, other methods: move or
  pass them); check overrides in sub/superclasses; declare it in the target; adapt references
  to the source (pass source as parameter or only the needed values); make the old method
  delegate, then replace calls and delete it (or keep delegating if it is public API).
- **Watch out**: polymorphic overrides; visibility; creating a circular dependency.
- **Treats**: Feature Envy, Shotgun Surgery, Inappropriate Intimacy, Parallel Inheritance
  Hierarchies, Message Chains, Data Class, Switch Statements (move the switch to the class that
  owns the type code).

## Move Field
- **When**: a field is used more by another class, or belongs with a moved method group.
- **Steps**: encapsulate the field first (Self Encapsulate Field); create field + accessors
  in target; decide how the source reaches the target; switch accessors to the target;
  remove the source field.
- **Watch out**: persistence mappings and serialized names.
- **Treats**: Shotgun Surgery, Data Clumps, Temporary Field.

## Extract Class
- **When**: one class does the work of two (disjoint clusters of fields/methods; subsets that
  change together).
- **Steps**: decide the split by responsibility; create the new class; link old → new;
  Move Field then Move Method, smallest/lowest-level first; decide whether to expose the new
  class (and as reference or value); rename the old class if its responsibility changed.
- **Watch out**: bidirectional links; do not create a Data Class + Feature Envy pair.
- **Treats**: Large Class, Divergent Change, Data Clumps, Primitive Obsession, Temporary Field.
- **Leads to**: Strategy/State/Bridge (when the extracted part varies), Facade (the old class).

## Inline Class
- **When**: a class does almost nothing (Lazy Class) or responsibilities moved away.
- **Steps**: create the public members in the absorbing class delegating to it; switch callers;
  move fields and methods in; delete the class.
- **Treats**: Lazy Class, Shotgun Surgery, Speculative Generality.

## Hide Delegate
- **When**: clients navigate `a.getB().doX()` and depend on `B`.
- **Steps**: add `a.doX()` delegating to `b`; replace client chains; hide accessor to `b` if
  nobody else needs it.
- **Watch out**: too many delegating methods produce Middle Man.
- **Treats**: Message Chains, Inappropriate Intimacy. **Leads to**: Facade.

## Remove Middle Man
- **When**: a class has many methods that only delegate.
- **Steps**: expose the delegate via an accessor; replace calls to delegating methods with
  direct calls; remove the delegating methods.
- **Watch out**: keep delegation that is a deliberate boundary (layering, Proxy, Facade).
- **Treats**: Middle Man, over-engineered wrappers.

## Introduce Foreign Method
- **When**: a library class lacks a method you need and you cannot change it.
- **Steps**: create the method in the client, taking the library object as first parameter;
  mark it as a candidate to move into a local extension; replace duplicates.
- **Language idioms**: extension functions (Kotlin, C#, Swift), traits (Rust), monkey patching
  is NOT a refactoring.
- **Treats**: Incomplete Library Class, Duplicate Code.

## Introduce Local Extension
- **When**: many foreign methods for the same library class.
- **Steps**: create a subclass (if the class allows) or a wrapper that holds the library object
  and delegates; move the foreign methods into it; use the extension type in your code.
- **Leads to**: Adapter / Decorator.
- **Treats**: Incomplete Library Class.
