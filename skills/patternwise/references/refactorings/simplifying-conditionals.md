# Simplifying Conditional Expressions

Conditionals tend to grow in complexity over time. These techniques make them readable and,
when they encode type-based variation, replace them with polymorphism.

Format: **When** · **Steps** · **Watch out** · **Treats**.

## Decompose Conditional
- **When**: a complex `if/else if/else` or `switch` with non-trivial conditions and branches.
- **Steps**: Extract Method on the condition (`isSummer(date)`); Extract Method on each branch
  (`summerCharge(...)`).
- **Treats**: Long Method, Comments.

## Consolidate Conditional Expression
- **When**: several conditions lead to the same result/action.
- **Steps**: verify conditions have no side effects; combine with `and`/`or` (sequential → or,
  nested → and); Extract Method with an intent-revealing name.
- **Treats**: Duplicate Code.

## Consolidate Duplicate Conditional Fragments
- **When**: the same code appears in all branches.
- **Steps**: move code common at the start before the conditional, at the end after it.
- **Watch out**: evaluation order and side effects inside conditions.
- **Treats**: Duplicate Code.

## Remove Control Flag
- **When**: a boolean variable steers a loop/flow (`done = true` ... `if (!done)`).
- **Steps**: replace setting the flag with `break`/`continue`/`return`; remove the flag.
- **Treats**: Long Method, readability.

## Replace Nested Conditional with Guard Clauses
- **When**: nested `if`s obscure the normal path; special cases buried deep.
- **Steps**: turn each special case into an early `return`/`throw` at the top; leave the main
  flow un-nested; consolidate guards with the same outcome.
- **Watch out**: functions that require a single exit (rare; check team style).
- **Treats**: Long Method, arrow-shaped code.

## Replace Conditional with Polymorphism
- **When**: a conditional selects behavior by object type/type code, especially if repeated in
  several places.
- **Prerequisites**: a hierarchy exists or is created via Replace Type Code with Subclasses or
  Replace Type Code with State/Strategy; the conditional is in its own method (Extract Method)
  and sits on the class that owns the type (Move Method).
- **Steps**: for each subclass, override the method with that branch's body; remove the branch
  from the conditional; when all branches are moved, make the base method abstract (or a
  sensible default); repeat for other conditionals on the same type code.
- **Watch out**: closed sum types with exhaustive matching may be the better idiom (see
  `language-idioms.md`); the variant-selection switch must still live somewhere — keep exactly
  one (factory).
- **Leads to**: Strategy, State, Command, Template Method.
- **Treats**: Switch Statements, Shotgun Surgery, Open/Closed violations.

## Introduce Null Object
- **When**: many `if (x == null)` checks that all do the same default.
- **Steps**: create a subclass/implementation representing "nothing" with neutral behavior; return
  it instead of null (from factories, finders, defaults); remove null checks that match its
  behavior; keep `isNull()` only if some clients truly need to distinguish.
- **Watch out**: it can hide real errors; do not use when absence must be handled explicitly.
  Languages with Option/Maybe/nullable types often prefer those.
- **Treats**: Switch Statements (null branch), Temporary Field.

## Introduce Assertion
- **When**: code silently assumes a condition (non-negative quantity, initialized dependency).
- **Steps**: add an assertion (or explicit check + exception if in production path) stating the
  assumption.
- **Watch out**: assertions must not change behavior; if disabled in production, behavior must
  not depend on them. If validating external input, that is validation, not an assertion.
- **Treats**: Comments, hidden assumptions.
