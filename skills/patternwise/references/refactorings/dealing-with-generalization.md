# Dealing with Generalization

Move functionality along inheritance hierarchies, extract/collapse abstractions, and switch
between inheritance and delegation. High leverage, higher risk: check overrides, LSP
(`principles.md`), and all subclasses before each step.

Format: **When** · **Steps** · **Watch out** · **Treats**.

## Pull Up Field
- **When**: subclasses have the same field.
- **Steps**: verify identical use; rename to a common name if needed; declare in parent (protected or
  private + accessors); remove from subclasses.
- **Treats**: Duplicate Code.

## Pull Up Method
- **When**: subclasses have methods doing the same work.
- **Steps**: make the bodies identical (Substitute Algorithm/Extract Method if needed); unify
  signatures; move to parent; remove subclass copies; if it uses subclass-only members, declare them
  abstract in the parent or pull them up too.
- **Treats**: Duplicate Code. **Leads to**: Template Method.

## Pull Up Constructor Body
- **When**: subclass constructors repeat the same initialization.
- **Steps**: create a parent constructor with the shared part; call it via `super(...)` first; keep
  subclass-specific code after.

## Push Down Method
- **When**: a parent method is used by only one/some subclasses.
- **Steps**: declare in the subclasses that need it; remove from parent; check callers that relied
  on the parent type.
- **Treats**: Refused Bequest.

## Push Down Field
- **When**: a field is used only by some subclasses.
- **Steps**: declare it in those subclasses; remove from parent.
- **Treats**: Refused Bequest.

## Extract Subclass
- **When**: some features are used only in some instances (often flagged by a type code or a
  boolean field).
- **Steps**: create the subclass; add a factory/constructor path to create it; Push Down methods and
  fields specific to that case; remove the flag/type code.
- **Watch out**: only one dimension of variation can be modeled by subclassing; for several or for
  runtime changes, prefer Replace Type Code with State/Strategy.
- **Treats**: Large Class.

## Extract Superclass
- **When**: two classes share fields and methods.
- **Steps**: create an abstract parent; make both extend it; Pull Up Field / Pull Up Method /
  Pull Up Constructor Body; use the parent type in clients where possible.
- **Watch out**: single-inheritance languages: the classes must not already have parents; consider
  Extract Class (composition) instead.
- **Treats**: Duplicate Code, Alternative Classes with Different Interfaces.

## Extract Interface
- **When**: clients use the same subset of a class's operations, or several classes share a role.
- **Steps**: declare an interface with the shared operations; implement it; switch client
  declarations to the interface.
- **Watch out**: one implementation and no seam need = Speculative Generality.
- **Leads to**: Strategy, Adapter, Proxy, Decorator, Composite (all rely on a common interface).
- **Treats**: Large Class (role split), Interface Segregation.

## Collapse Hierarchy
- **When**: a subclass is practically the same as its parent.
- **Steps**: choose which one to remove; Pull Up or Push Down all members; replace references; delete.
- **Treats**: Lazy Class, Speculative Generality; removes over-engineering.

## Form Template Method
- **When**: subclasses implement algorithms with the same steps in the same order, differing in details.
- **Steps**: Extract Method so each subclass algorithm becomes a sequence of step calls; give identical
  steps the same name and Pull Up Method; differing steps get the same signature and become abstract
  (or hook with default) in parent; Pull Up the now-identical skeleton method.
- **Leads to**: Template Method. Functional alternative: pass the varying steps as functions.
- **Treats**: Duplicate Code.

## Replace Inheritance with Delegation
- **When**: a subclass uses only part of the parent, or inheritance exists only for reuse (no real
  is-a), or behavior must be swapped/combined at runtime.
- **Steps**: add a field holding a parent instance; make subclass methods delegate to it instead of
  `super`; add delegating methods for the parent methods clients use; remove the inheritance;
  initialize the field (constructor/injection).
- **Watch out**: identity checks, protected members used by the subclass, framework requirements to
  subclass.
- **Leads to**: Decorator, Strategy, Bridge, Proxy, Adapter.
- **Treats**: Refused Bequest, combinatorial subclass explosion.

## Replace Delegation with Inheritance
- **When**: a class delegates to *all* methods of a delegate, and the is-a relation genuinely holds.
- **Steps**: make the class a subclass of the delegate; remove delegating methods; remove the field.
- **Watch out**: rarely the right move; it makes the class expose the whole parent interface and couples it to it. Prefer language delegation features (Kotlin `by`) when available.
- **Treats**: Middle Man.
