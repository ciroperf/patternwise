# Simplifying Method Calls

Make interfaces between classes easy to understand and use. Signature changes ripple to
callers: find all of them (LSP "find references", grep, public API consumers) first.

Format: **When** · **Steps** · **Watch out** · **Treats**.

## Rename Method
- **When**: the name does not explain what the method does.
- **Steps**: check overrides/implementations; rename via tooling; for public APIs add the new name
  and deprecate the old one delegating to it.
- **Treats**: Alternative Classes with Different Interfaces, Comments.

## Add Parameter
- **When**: a method needs data it cannot reach.
- **Steps**: add the new method/overload with the parameter; switch callers; remove old version.
- **Watch out**: often a sign you should Move Method or use Introduce Parameter Object instead.

## Remove Parameter
- **When**: a parameter is unused.
- **Steps**: check overrides that might use it; remove; update callers.
- **Treats**: Speculative Generality, Long Parameter List.

## Separate Query from Modifier
- **When**: a method returns a value **and** changes state.
- **Steps**: create a side-effect-free query returning the value; make the original a pure
  modifier (void); update callers to call both.
- **Watch out**: concurrency — atomic check-and-act may need to stay together (document why).

## Parameterize Method
- **When**: several methods do the same with different constants (`raise5pc`, `raise10pc`).
- **Steps**: create one method with a parameter; replace bodies of old methods with calls; replace
  callers; delete old methods.
- **Treats**: Duplicate Code.

## Replace Parameter with Explicit Methods
- **When**: a method branches on a parameter value (often a flag/enum) into distinct behaviors.
- **Steps**: create one method per value; replace callers that pass constants; remove the original.
- **Treats**: Switch Statements, Long Method, boolean flag arguments.

## Preserve Whole Object
- **When**: callers extract several values from one object to pass them.
- **Steps**: add a parameter for the whole object; read values from it inside; remove the single
  parameters.
- **Watch out**: adds a dependency on the whole type; fine when the callee is in the same domain.
- **Treats**: Long Parameter List, Data Clumps, Primitive Obsession, Long Method.

## Replace Parameter with Method Call
- **When**: the caller computes a value the callee could compute itself.
- **Steps**: inside the callee, obtain the value directly; remove the parameter.
- **Treats**: Long Parameter List.

## Introduce Parameter Object
- **When**: a group of parameters repeats across methods.
- **Steps**: create an (immutable) class for the group; add it as a parameter; move uses one by one;
  remove the old parameters; move behavior that works on the group into the new class.
- **Leads to**: Value Object; sometimes Builder.
- **Treats**: Long Parameter List, Data Clumps, Primitive Obsession.

## Remove Setting Method
- **When**: a field should be set only at creation.
- **Steps**: initialize via constructor; remove the setter; make the field final/readonly.

## Hide Method
- **When**: a method is not used outside its class (or hierarchy).
- **Steps**: reduce visibility to the minimum; run build/tests.
- **Treats**: Data Class (overly broad accessors).

## Replace Constructor with Factory Method
- **When**: construction needs logic (choosing a subclass, caching, named variants), or a type
  code is about to become subclasses.
- **Steps**: create a static/factory method calling the constructor; replace constructor calls;
  make the constructor private/internal when possible.
- **Leads to**: Factory Method (pattern), Abstract Factory, Flyweight/registry.

## Replace Error Code with Exception
- **When**: a method returns special values (-1, null, false) to signal errors.
- **Steps**: decide checked vs unchecked (follow project convention); throw instead of returning
  the code; update callers to catch/propagate.
- **Watch out**: follow the project's error model — in Go, Rust, or Result-based code, error
  values ARE idiomatic; do not introduce exceptions there.

## Replace Exception with Test
- **When**: an exception is used for a condition the caller could check up front.
- **Steps**: add the conditional check before the call; keep the exception for truly unexpected cases.
- **Watch out**: race conditions (TOCTOU) with files/network: then exceptions are correct.
