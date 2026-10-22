# Memento (Behavioral)

**Intent**: capture and restore an object's previous state without exposing its internals.

## Problem it solves
- Undo, rollback, checkpoints or drafts implemented by external code reading/writing the
  object's fields (breaking encapsulation, or forcing everything public).
- Transactions that must roll back an object to its previous state on error.

## Roles
- **Originator**: creates snapshots of its own state and restores from them.
- **Memento**: immutable snapshot; opaque to everyone but the originator.
- **Caretaker**: keeps a history of mementos and decides when to restore; never inspects them.

## Recognize it
- `save()/snapshot()/createMemento()` returning an opaque object and `restore(m)`; history stacks
  in editors; serialized state checkpoints.

## Red flags
- Caretaker reading memento fields → encapsulation lost.
- Mementos holding references to mutable live objects (shallow snapshot) → restore is wrong.
- Unbounded history → memory growth.

## Don't use when
- State is already immutable (keep previous versions directly) or undo is not required.

## Idiomatic forms
- Immutable state + history list (Redux-style), `copy`/`dataclasses.replace`, serialization
  snapshots, nested classes/private types for opacity.

## Path to it
Encapsulate Field (stop external access) → Extract Class for the snapshot data → move
save/restore into the originator → caretaker keeps snapshots only.

## Trade-offs
+ Snapshots without breaking encapsulation; simplifies originator. − Memory cost; caretakers must
manage lifecycle; hard in languages without strong encapsulation.

## Related
Used with Command for undo; with Iterator to save traversal state; Prototype can be a simpler
alternative when the object is easy to clone.
