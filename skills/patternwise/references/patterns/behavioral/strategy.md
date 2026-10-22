# Strategy (Behavioral)

**Intent**: define a family of interchangeable algorithms, put each in a separate unit, and let
the context use any of them through a common interface.

## Problem it solves
- A class grows a conditional that selects among variants of an algorithm (pricing rules,
  routing, compression, sorting, export format), and new variants keep coming.
- Several near-duplicate classes differ only in one algorithm.
- The algorithm must be chosen at runtime (config, user choice, A/B test).

## Roles
- **Context**: holds a reference to a Strategy; delegates the algorithm to it.
- **Strategy** interface: one (or few) methods.
- **Concrete Strategies**: the variants.
- **Client**: picks the strategy and passes it to the context.

## Recognize it
- A field/parameter typed as an interface or a function type that the context calls to perform one
  job; implementations selected outside the context; comparator/key functions.

## Red flags
- Only one strategy and no realistic second → over-engineering (Speculative Generality).
- Strategy chosen by a switch inside the context every call → the conditional was not removed,
  just moved; select once.
- Strategies needing many context internals (large parameter lists, back references) → wrong
  boundary.
- Strategies that change the context's state and swap themselves → that is State.

## Don't use when
- Variants are two, stable, and trivial: an `if` or a parameter is clearer.

## Idiomatic forms
- Pass a function/lambda; dict of functions keyed by variant; `Comparator`, `key=`; Go function
  types; C++ policy templates.

## Path to it
Extract Method for each branch → Replace Type Code with State/Strategy or Extract Interface over
the algorithms → Replace Conditional with Polymorphism → move the choice to the client/composition
root (Factory if needed). Substitute Algorithm when variants share a goal.

## Trade-offs
+ Swap algorithms at runtime; isolates algorithm details; OCP; composition over inheritance.
− Clients must know the differences between strategies; more units for few variants.

## Related
Bridge, State, Command share the composition-based shape with different intents. Template Method
varies steps by inheritance; Strategy varies the whole algorithm by composition. Decorator changes
the skin, Strategy the guts.
