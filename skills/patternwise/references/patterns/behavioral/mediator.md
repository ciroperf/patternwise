# Mediator (Behavioral)

**Intent**: reduce chaotic many-to-many dependencies by making components communicate only
through a mediator object that coordinates them.

## Problem it solves
- Components (form widgets, services, aircraft) reference each other directly; changing one
  ripples to many (Inappropriate Intimacy, Shotgun Surgery); components cannot be reused elsewhere
  because they are wired to their peers.
- Many component subclasses exist only to reuse basic behavior in different contexts; a new
  mediator per context would let the same components collaborate differently.

## Roles
- **Components**: hold a reference to the Mediator interface only; notify it of events.
- **Mediator** interface: `notify(sender, event)`.
- **Concrete Mediator**: knows the components and implements the coordination rules.

## Recognize it
- A dialog/controller/coordinator that receives events from children and tells other children what
  to do; children never reference siblings; message brokers/orchestrators at service level.

## Red flags
- The mediator becomes a God object holding all business logic → split by use case.
- Components still calling each other directly besides the mediator.
- Mediator for two components that interact in one way → unneeded.

## Don't use when
- Interactions are few and stable.

## Idiomatic forms
- UI controllers/view-models, MediatR-style request dispatch (note: that library is closer to a
  Command bus), event aggregators, workflow orchestrators.

## Path to it
Extract Class for coordination logic scattered among components → Move Method into it → Change
Bidirectional Association to Unidirectional (components → mediator) → Extract Interface for the
mediator.

## Trade-offs
+ Components decoupled and reusable; interactions in one place. − Mediator can grow into a God
object.

## Related
Facade organizes access to a subsystem whose classes do not know it; Mediator's components do.
Observer can implement the mediator's notification (dynamic subscriptions). CoR, Command,
Mediator, Observer are all ways to connect senders and receivers.
