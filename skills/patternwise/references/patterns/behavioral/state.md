# State (Behavioral)

**Intent**: let an object change its behavior when its internal state changes, as if it changed
class — by delegating state-specific behavior to state objects.

## Problem it solves
- Methods full of `if (status == DRAFT) ... else if (status == REVIEW) ...`, repeated across many
  methods, with transitions scattered and illegal transitions possible (finite state machine
  hidden in conditionals).
- Many states whose state-specific code changes often; temporary fields and helpers used only
  in some states; duplicate code across similar states and transitions.

## Roles
- **Context**: holds the current State; delegates state-dependent work; exposes a way to change state.
- **State** interface: state-specific methods.
- **Concrete States**: implement behavior for one state and decide transitions (set the next
  state on the context).

## Recognize it
- A `state` field typed as an interface whose implementations call `context.setState(new X())`;
  workflow/order/document lifecycles; protocol handlers.

## Red flags
- States as an enum + switch in every method (State **missing**, smell: Switch Statements) when
  states/transitions are many and growing.
- State classes that are pure data (no behavior) → just an enum.
- Transitions both in context and in states → split brain.
- Two states only, few methods → pattern is overkill.

## Don't use when
- Few states, rarely changing, simple behavior: an enum + small switch or a transition table is
  clearer.

## Idiomatic forms
- Transition table/dict `{(state, event): next_state}` for simple FSMs; sealed classes/enums with
  methods (Kotlin, Java enum with abstract methods, Rust enums + match + typestate pattern);
  state-machine libraries (XState, Spring Statemachine).

## Path to it
Replace Type Code with State/Strategy → Extract Method per state-dependent branch → Replace
Conditional with Polymorphism into state classes → Move transition logic into states.

## Trade-offs
+ SRP per state; OCP for new states; removes duplicated conditionals. − Overkill for small
machines; transitions spread across classes may be harder to see as a whole.

## Related
Same structure as Strategy, but states know each other and drive transitions. State objects
without fields can be shared (Flyweight/Singleton).
